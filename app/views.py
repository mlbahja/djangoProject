from django.shortcuts import render
from django.http import HttpResponse

def HelloWorld(Request):
    return HttpResponse("Hello World")
# Create your views here.
