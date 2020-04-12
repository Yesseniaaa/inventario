from django.db import models
from salidas.models import Recinto, Funcionario
from .validators import *


class Activofijo(models.Model):
    id_activo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    cod_barra = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=100)
    id_funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    id_recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.nombre)
