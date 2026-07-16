from django.urls import path
from . import views

urlpatterns = [
    #vistas general
    path('',views.solicitudes, name="solicitudes"),
    path('borrar/<int:nro>',views.solicitudes_borrar_uno, name="borrar_peticion_uno"),
    path('borrar/todo',views.solicitudes_borrar_todo, name="borrar_peticion_todo"),
    
    #vistas editar
    
    path('editar', views.editor, name='editar'),
    path('editar/<int:nro>', views.editor_id, name='editar_peticion'),
    path('editar/guardar', views.editor_guardar, name='guardar_peticion'),
    
    #vistas ejecutar
    path('respuestas',views.respuestas, name="respuestas")
]