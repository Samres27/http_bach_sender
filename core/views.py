from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import loader
from django.db.models import Max
from .models import Peticiones
from .utils.socket_sender import enviarPeticiones
import re
import json

# ----------- SOLICITUDES ------------
def solicitudes(request):
    total_peticiones=Peticiones.objects.all().values()
    template = loader.get_template('solicitudes.html')
    contenido={
        "peticiones": total_peticiones,
    }
    return HttpResponse(template.render(context=contenido))

def solicitudes_borrar_uno(request,nro):
    print(nro)
    Peticiones.objects.get(nroPeticion=nro).delete()
    return redirect("solicitudes")

def solicitudes_borrar_todo(request):
    Peticiones.objects.all().delete()
    return redirect("solicitudes")

# ----------- EDITOR ------------
def editor(request):
    template = loader.get_template('editor.html')
    return HttpResponse(template.render())

def editor_id(request,nro):
    peticion_select= Peticiones.objects.get(nroPeticion=nro)
    template = loader.get_template('editor.html')
    contenido={
        'peticion':peticion_select,   
    }
    print(contenido,peticion_select.dominio)
    return HttpResponse(template.render(context=contenido))

def editor_guardar(request):
    if request.method == "POST":
        re_match=r"^https"
        cuerpo=json.loads(request.body)
        try:
            nroP=int(cuerpo["nroPeticion"])
            if nroP==0:
                max_num = Peticiones.objects.aggregate(Max('nroPeticion'))['nroPeticion__max']
                if max_num is None:
                    nroP=1
                else:
                    nroP=max_num+1
                
                nuevoPeticion=Peticiones(nroPeticion=nroP,
                        metodo=cuerpo["metodo"],
                        dominio=cuerpo["dominio"],
                        url=cuerpo["url"],
                        https=re.match(re_match,cuerpo["dominio"]) != None,
                        peticion=cuerpo["peticion"],
                        respuesta="")
                nuevoPeticion.save()
            else:
                ## actualizar peticcion
                act_peticion=Peticiones.objects.get(id=nroP)
                act_peticion.metodo=cuerpo["metodo"]
                act_peticion.dominio=cuerpo["dominio"]
                act_peticion.url=cuerpo["url"]
                act_peticion.https=re.match(re_match,cuerpo["dominio"]) != None
                act_peticion.peticion=cuerpo["peticion"]
                act_peticion.save()
                
        except Exception as e:
            print(e)
            return HttpResponse(status=400,content=b'Datos en la peticion no validos')

        return HttpResponse(status=200)
    
    return HttpResponseNotAllowed(['POST'], content=b'')


# ----------- RESPUESTAS ------------
def procesarPeticiones(request):
    peticiones=Peticiones.objects.all().values()
    resp=enviarPeticiones(peticiones)
    for x in resp:
        peticion_select= Peticiones.objects.get(nroPeticion=x["nro"])
        peticion_select.respuesta=x["respuesta"]
        peticion_select.codigo_respuesta=x["status"]
        peticion_select.save()

def respuestas(request):
    total_peticiones=Peticiones.objects.all().values()
    contenido={
        "peticiones": total_peticiones,
    }
    template = loader.get_template('respuestas.html')
    return HttpResponse(template.render(context=contenido))