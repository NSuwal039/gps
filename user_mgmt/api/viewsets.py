from rest_framework.viewsets import ModelViewSet
from .serializers import *
from ..models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    
    def get_queryset(self):
        return Organization.objects.all()

class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    
    def get_queryset(self):
        return Department.objects.all()

class PersonViewSet(ModelViewSet):
    serializer_class = PersonSerializer
    
    def get_queryset(self):
        return Person.objects.all()

class GPSViewSet(ModelViewSet):
    serializer_class = GPSSerializer
    
    def get_queryset(self):
        return GPS.objects.all()

class LocationDataViewSet(ModelViewSet):
    serializer_class = LocationDataSerializer
    
    def get_queryset(self):
        return LocationData.objects.all()

@api_view
def stream_gps_data(request, imei:str):
    pass