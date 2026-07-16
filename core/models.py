from django.db import models

class Peticiones(models.Model):
    nroPeticion = models.IntegerField()
    metodo = models.CharField(max_length=255)
    dominio = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    https=models.BooleanField()
    peticion = models.CharField()
    respuesta = models.CharField()
    