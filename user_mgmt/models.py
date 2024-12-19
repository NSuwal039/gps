from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class OwnerType(models.TextChoices):
    ORGANIZATION = 'O', _('Organization')
    DEPARTMENT = 'D', _('Department')
    PERSON = 'P', _('Person')
    ADMIN = 'A', _('Admin')

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=1, choices=OwnerType)
    
    class Meta:
        db_table = 'auth_user'

    def get_associated_entity(self):
        if self.user_type == 'O':
            return self.organization
        if self.user_type == 'D':
            return self.department
        if self.user_type == 'P':
            return self.person
        return None

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(255, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Person(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    
class GPS(models.Model):
    imei = models.CharField(max_length=15, primary_key=True)
    brand = models.CharField(null=True, blank=True)
    
    owner_type = models.CharField(max_length=1, choices=OwnerType, default=OwnerType.DEPARTMENT)
    owner_org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    owner_dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    owner_person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                name = '%(app_label)s_%(class)s_only_one_owner',
                check=(
                    models.Q(owner_type = OwnerType.PERSON, owner_org__isnull=True, owner_dept__isnull=True, owner_person__isnull=False)|
                    models.Q(owner_type = OwnerType.DEPARTMENT, owner_org__isnull=True, owner_dept__isnull=False, owner_person__isnull=True)|
                    models.Q(owner_type = OwnerType.ORGANIZATION, owner_org__isnull=False, owner_dept__isnull=True, owner_person__isnull=True)
                )
            )
        ]
    
    def get_owner(self):
        if self.owner_org!=None:
            return self.owner_org
        return self.owner_dept if self.owner_dept!=None else self.owner_person 

class LocationData(models.Model):
    gps_imei = models.ForeignKey(GPS, on_delete=models.CASCADE)
    time = models.DateTimeField()
    latitude = models.CharField(max_length=12)
    longitude = models.CharField(max_length=12)
    speed = models.IntegerField(default=0)
    course = models.CharField(max_length=5)
    
    class Meta:
        indexes = [
            models.Index(fields=['gps_imei', '-time'])
        ]