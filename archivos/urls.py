from django.urls import path
from . import views

urlpatterns = [
    path("subir/", views.subir_archivo, name="subir_archivo"),
    path('guardar/', views.guardar_archivo, name='guardar_archivo'),
]