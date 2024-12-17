from django.shortcuts import render
import asyncio
from datetime import datetime
from django.http import StreamingHttpResponse, HttpResponse
import json
import redis.asyncio as redis
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
import jwt
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from user_mgmt.models import LocationData, GPS

# Create your views here.

def return_something(request):
    return HttpResponse('Hello')

async def _listen_to_redis(pubsub):         # if timeout is needed
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message is not None:
            return message
        await asyncio.sleep(0.1)
        
async def stream_event(client:redis.Redis, imei:str,request):
    pubsub = client.pubsub()
    await pubsub.subscribe(imei)
    
    latest_data = LocationData.objects.filter(gps=imei).values(
        'latitude', 'longitude', 'time','speed','course'
    ).order_by('-time')[0]
    print(latest_data)
    
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                print(message, type(message))
                channel = message['channel'].decode('utf-8')  # Converts bytes to string
                decoded_data = message['data'].decode('utf-8')
                parsed_data = json.loads(decoded_data)
                # parsed_channel = json.loads(channel)
                parsed_data['channel'] = channel
                print(channel)
                yield f"data: {parsed_data} \n\n"
                             
    except asyncio.CancelledError:
        print('In cancelled error')
        # Cleanup when cancelled
        await pubsub.unsubscribe()
        await pubsub.close()
    finally:
        print('In finally')
        await pubsub.unsubscribe()
        await pubsub.close()  
        await client.close()
        
# @jwt_required
async def stream_time(request, imei:str):
    
    # auth within view because couldnt run decorator or API auths
    token = request.headers.get('Authorization', None)
    print(token)
    if not token:
        raise AuthenticationFailed('No token provided in request.')
    try:
        payload = jwt.decode(
            token.split(' ')[1],
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        # request.user = payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired.')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token.')
    
    client = await redis.Redis(host='localhost', port=6379, db=0)
    response = StreamingHttpResponse(stream_event(client, imei, request), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['Access-Control-Allow-Origin'] = '*'  # Allow all domains (can be modified for security)
    response['Access-Control-Allow-Methods'] = 'GET'
    response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, X-Requested-With'
    # response['Connection'] = 'keep-alive'
    
    # # Ensure proper cleanup when the response is finished
    # # response.streaming_content.aclose()
    await client.close()
    print('Client connection closed, stopping stream.')
    return response
