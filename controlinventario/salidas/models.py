from django.db import models
from django.db.models import Sum
from inventario.models import Producto
from django.urls import reverse
from .validators import ValidateMayorCero, ValidateRut, ValidateLength, validate_dob, ValidarTelefono
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime



class Recinto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True)
    estado = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.nombre)


class Funcionario(models.Model):
    id = models.AutoField(primary_key=True)
    id_recinto = models.ManyToManyField(Recinto)
    rut = models.CharField(max_length=15, unique=True, validators=[ValidateRut])
    nombres = models.CharField(max_length=40)
    paterno = models.CharField(max_length=40)
    materno = models.CharField(max_length=40)
    mail = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=9, validators=[ValidarTelefono])
    estado = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.nombres)

class Salida(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    id_funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    id_recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    total = models.IntegerField()
    productos = models.ManyToManyField(Producto, through="Sal_prod")

    def __str(self):
        return "SalidaID: " + str(self.id)

class Sal_prod(models.Model):
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_salida = models.ForeignKey(Salida, on_delete=models.CASCADE)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id_salida)

class Prestamo(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    id_funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    id_recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    total = models.IntegerField()
    devolucion = models.DateField()
    productos = models.ManyToManyField(Producto, through="Pre_prod")

    def __str(self):
        return "PrestamoID: " + str(self.id)

class Pre_prod(models.Model):
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id_salida)