from rest_framework.viewsets import ModelViewSet
from .serializers import *
from ..models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.db import transaction

class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    
    def get_queryset(self):
        return Organization.objects.all()
    
    @transaction.atomic
    def create(self, request):
        org_data = request.data.get('organization')
        user_data = request.data.get('user')
        if org_data == None:
            return Response(
                {'error': 'Organization data not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )            
        
        if user_data == None:
            return Response(
                {'error': 'User data not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )            
        
        user_data['user_type']='O'
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            transaction.set_rollback(True)
            return Response(
                {'errors': user_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = user_serializer.save()
        
        org_data['user']=user.pk
        org_serializer = self.get_serializer(data=org_data)
        if not org_serializer.is_valid():
            return Response(
                {'error':org_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            org_serializer.save()
            
            return Response(
                org_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            transaction.set_rollback(True)
            
            return Response(
                {'error':e},
                status=status.HTTP_400_BAD_REQUEST
            )

class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    
    def get_queryset(self):
        return Department.objects.all()
    
    @transaction.atomic
    def create(self, request):
        dept_data = request.data.get('department')
        user_data = request.data.get('user')
        if dept_data == None:
            return Response(
                {'error': 'Department data not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )            
        
        if user_data == None:
            return Response(
                {'error': 'User data not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )            
            
        user_data['user_type']='D'
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response(
                {'errors': user_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = user_serializer.save()
        dept_data['user']=user.pk
        dept_serializer = self.get_serializer(data=dept_data)
        if not dept_serializer.is_valid():
            transaction.set_rollback(True)
            return Response(
                {'error':dept_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            dept_serializer.save()
            return Response(
                dept_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            transaction.set_rollback(True)
            return Response(
                {'error':e},
                status=status.HTTP_400_BAD_REQUEST
            )

class PersonViewSet(ModelViewSet):
    serializer_class = PersonSerializer
    
    def get_queryset(self):
        return Person.objects.all()
    
    @transaction.atomic
    def create(self, request):
        person_data = request.data.get('person')
        user_data = request.data.get('user')
        if person_data == None:
            return Response(
                {'error': 'Personnel data not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )            
        
        if user_data == None:
            return Response(
                {'error': 'User data not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )            
            
        user_data['user_type']='P'
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response(
                {'errors': user_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = user_serializer.save()
        
        person_data['user']=user.pk
        person_serializer = self.get_serializer(data=person_data)
        if not person_serializer.is_valid():
            transaction.set_rollback(True)
            return Response(
                {'error':person_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            person_serializer.save()
            
            return Response(
                person_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            transaction.set_rollback(True)
            
            return Response(
                {'error':e},
                status=status.HTTP_400_BAD_REQUEST
            )


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