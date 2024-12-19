from django.shortcuts import render
from django.http.response import HttpResponse
from django.db.models import Prefetch
from .models import *
import json
import time
from django.db import connection
# Create your views here.

def hello(request):
    return HttpResponse('Hello')

def generate_gps_dict(gps_list:list):
    return[
        {
            'imei':gps.imei,
            'brand':gps.brand,
            'owner_type':gps.owner_type,
            'owner_id':gps.get_owner().id
        } for gps in gps_list
    ]

def org_with_gps(org_id):
    org = Organization.objects.select_related('user').prefetch_related(
        Prefetch('department_set', queryset=Department.objects.select_related('user').prefetch_related(
            Prefetch('person_set', queryset=Person.objects.select_related('user').prefetch_related('gps_set')),
            Prefetch('gps_set')
        )),
        Prefetch('gps_set')
    ).get(id=org_id)
    
    person_gps = [gps for dept in org.department_set.all() for person in dept.person_set.all() for gps in person.gps_set.all()]
    dept_gps = [gps for dept in org.department_set.all() for gps in dept.gps_set.all()]
    org_gps = [gps for gps in org.gps_set.all()]
    
    combined_gps_list = generate_gps_dict(person_gps+dept_gps+org_gps)

    department_list = [
        {
            'dept_id':dept.id,
            'dept_name':dept.name,
            'user_id':dept.user.id,
        } for dept in org.department_set.all()  
    ]
    
    person_list = [
        {
            'person_id':person.id,
            'user_id':person.user.id,
            'dept_id':person.department.id
        }for dept in org.department_set.all() for person in dept.person_set.all()
    ] 
    
    final_data = {
        'org_id':org.id,
        'user_id':org.user.id,
        'org_name':org.name,
        'dept_list':department_list,
        'person_list':person_list,
        'gps_list':combined_gps_list
    }
    
    # for query in connection.queries:
    #     print(f"SQL Query: {query['sql']}")
    #     print(f"Execution Time: {query['time']} seconds")
    return(final_data)    

def dept_with_gps(request):
    dept = Department.objects.select_related('user').prefetch_related(
        Prefetch('person_set',queryset=Person.objects.select_related('user').prefetch_related('gps_set')),
        Prefetch('gps_set')
    ).get(id=1)
    
    dept_gps_list = [gps for gps in dept.gps_set.all()]
    persons_gps_list = [gps for person in dept.person_set.all() for gps in person.gps_set.all()]
    
    combined_gps_list = generate_gps_dict(dept_gps_list+persons_gps_list)
    
    person_list = [
        {
            'person_id':person.id,
            'user_id':person.user.id,
            'dept_id':person.department.id
        }for person in dept.person_set.all()
    ] 
    
    # for query in connection.queries:
    #     print(f"SQL Query: {query['sql']}")
    #     print(f"Execution Time: {query['time']} seconds")
    final_data = {
        'dept_id':dept.id,
        'dept_name':dept.name,
        'gps_list':combined_gps_list,
        'person_list':person_list
    }
    
    return final_data