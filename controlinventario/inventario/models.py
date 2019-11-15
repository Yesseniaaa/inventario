from django.db import models
from .validators import *

ESTADOS = (
    ('pendiente', 'Pendiente'),
    ('inventariado', 'Inventariado'),
)

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True)
    estado = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.nombre)

class Producto(models.Model):
    id_prod = models.AutoField(primary_key=True)
    id_cat = models.ManyToManyField(Categoria)
    nombre = models.CharField(max_length=50)
    cod_barra = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=100)
    precio_compra = models.IntegerField(validators=[ValidateMayorCero])
    stock = models.IntegerField(validators=[ValidateNumeroPositivo], default=0)
    stock_min = models.IntegerField(validators=[ValidateNumeroPositivo], default=0)
    merma = models.IntegerField(validators=[ValidateNumeroPositivo], default=0)
    codigo = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=20, default='pendiente', choices=ESTADOS)
    estado_prod = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.nombre)

class RegistroTemporalProducto(models.Model):
    precio_compra = models.IntegerField(validators=[ValidateMayorCero], null=True, blank=True)
    stock = models.IntegerField(validators=[ValidateMayorCero], null=True, blank=True)
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
