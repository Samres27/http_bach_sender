from django.urls import path
from . import views

urlpatterns = [
    #vistas general
    path('',views.solicitudes, name="solicitudes"),
    path('borrar/<int:peticion>',views.solicitudes, name="borrar_peticion_uno"),
    path('borrar/todo',views.solicitudes, name="borrar_peticion_todo"),
    
    #vistas editar
    path('editar', views.editor, name='editar'),
    
    #vistas ejecutar
    path('respuestas',views.respuestas, name="respuestas")
]