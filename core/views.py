from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def editor(request):
    template = loader.get_template('editor.html')
    return HttpResponse(template.render())

def solicitudes(request):
    template = loader.get_template('solicitudes.html')
    return HttpResponse(template.render())

def respuestas(request):
    template = loader.get_template('respuestas.html')
    return HttpResponse(template.render())