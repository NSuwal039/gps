from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import *
from django.contrib.auth.models import Group, User
from django.conf import settings

class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        
class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class PersonSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class GPSSerializer(ModelSerializer):
    class Meta:
        model = GPS
        fields = '__all__'


class LocationDataSerializer(ModelSerializer):
    class Meta:
        model = LocationData
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    group = serializers.SerializerMethodField()
    
    def get_group(self, obj):
        if isinstance(obj, dict):
            return None
        return [item.name for item in obj.groups.all()]
            
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name','group', 'is_superuser']