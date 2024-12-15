from django.shortcuts import render
import asyncio
from datetime import datetime
from django.http import StreamingHttpResponse, HttpResponse
import json
import redis.asyncio as redis
from jwt_test.decorators import jwt_required
# Create your views here.

def return_something(request):
    return HttpResponse('Hello')

async def _listen_to_redis(pubsub):
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message is not None:
            return message
        await asyncio.sleep(0.1)
        
async def stream_event(client:redis.Redis, imei:str,request):
    timeout_count = 0
    pubsub = client.pubsub()
    await pubsub.subscribe(imei)
    try:
        while True:
            try:
                message = await asyncio.wait_for(
                    _listen_to_redis(pubsub),
                    timeout=15
                )
                print(f'message: {message == None}')
                if message is not None:
                    print(message, type(message))
                    channel = message['channel'].decode('utf-8')  # Converts bytes to string
                    decoded_data = message['data'].decode('utf-8')
                    parsed_data = json.loads(decoded_data)
                    # parsed_channel = json.loads(channel)
                    parsed_data['channel'] = channel
                    print(channel)
                    timeout_count = 0
                    yield f"data: {parsed_data} \n\n"
            except asyncio.TimeoutError:
                timeout_count+=1
                print(f'Timeout count: {timeout_count}')
                yield f'data: GPS data timeout. Count: {timeout_count} \n\n'
                
                if timeout_count >= 5:
                    print(f'GPS timeout count exceeded. Disconnecting.')
                    yield "data: Error. Timeout count exceeded. Disconnecting."   
                    break
                             
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