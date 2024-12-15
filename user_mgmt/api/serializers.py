from rest_framework.serializers import ModelSerializer
from ..models import *

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
