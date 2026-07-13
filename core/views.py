from django.shortcuts import render
from django.http import HttpResponse

def editor(request):
    return HttpResponse("Hello world! editor")

def solicitudes(request):
    return HttpResponse("Hello world! solicitudes")

def respuestas(request):
    return HttpResponse("Hello world! respuesta")