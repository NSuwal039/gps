from django.shortcuts import render
from jwt_test.decorators import jwt_required
from django.http.response import HttpResponse
# Create your views here.

@jwt_required
def hello(request):
    return HttpResponse('Hello')