from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# Create your models here.

user_model = get_user_model()
class OwnerType(models.TextChoices):
    ORGANIZATION = 'O', _('Organization')
    DEPARTMENT = 'D', _('Department')
    PERSON = 'P', _('Person')

class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(255, null=True, blank=True)
    user = models.OneToOneField(user_model, on_delete=models.CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.OneToOneField(user_model, on_delete=models.CASCADE)

class Person(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.OneToOneField(user_model, on_delete=models.CASCADE)    
    
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
                    models.Q(owner_type = OwnerType.ORGANIZATION, owner_org__isnull=False, owner_dept__isnull=False, owner_person__isnull=True)
                )
            )
        ]

class LocationData(models.Model):
    gps_imei = models.ForeignKey(GPS, on_delete=models.CASCADE)
    time = models.DateTimeField()
    latitude = models.CharField(max_length=12)
    longitude = models.CharField(max_length=12)
    speed = models.IntegerField(default=0)
    course = models.CharField(max_length=5)
    
    class Meta:
        indexes = [
            models.Index(fields=['gps_imei', 'time'])
        ]