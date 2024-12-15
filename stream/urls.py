from django.urls import path
from .views import stream_time, return_something

urlpatterns = [
    path('sse/<str:imei>/',stream_time, name='sse_stream'),
    path('test/', return_something, name='test'),
]
