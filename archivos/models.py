from django.db import models

# Create your models here.

from django.db import models

class ArchivoCargado(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10)  # Excel/CSV
    fecha_carga = models.DateTimeField(auto_now_add=True)
    columnas = models.TextField()  # lista de columnas como string
    filas = models.IntegerField()

    def __str__(self):
        return self.nombre