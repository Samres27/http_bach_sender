from django.urls import path
from . import views

urlpatterns = [
    path('editar', views.editor, name='editar'),
    path('',views.solicitudes, name="solicitudes"),
    path('respuestas',views.respuestas, name="respuestas")
]