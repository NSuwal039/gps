from rest_framework.routers import DefaultRouter
from user_mgmt.api.viewsets import *

router = DefaultRouter()
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('persons', PersonViewSet, basename='persons')
router.register('trackers', GPSViewSet, basename='gps')
router.register('location-data', LocationDataViewSet, basename='location-data')
