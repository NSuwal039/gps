from django.shortcuts import render
from django.http.response import HttpResponse
from django.db.models import Prefetch
from .models import *
# Create your views here.

def hello(request):
    return HttpResponse('Hello')

def org_with_gps(request):
    org = Organization.objects.prefetch_related(
        Prefetch('department_set', queryset=Department.objects.prefetch_related(
        Prefetch('person_set', queryset=Person.objects.prefetch_related(
            Prefetch('gps_set', queryset=GPS.objects.all())
        )),
        Prefetch(
            'gps_set', queryset=GPS.objects.all()
        ) 
        )),
        Prefetch(
            'gps_set', queryset=GPS.objects.all()
        )
    ).get(name='Organization 1')
    
    print(org.gps_set.all())
    print(
        [(dept.name, dept.gps_set.all()) for dept in org.department_set.all()]
    )
    print(
        [(dept.name, (person, person.gps_set.all())) for dept in org.department_set.all() for person in dept.person_set.all()]
    )
        
    return HttpResponse(org)
    
    

