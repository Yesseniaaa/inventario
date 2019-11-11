from django.db import models
from inventario.models import Producto, RegistroTemporalProducto
from .validators import ValidateMayorCero, ValidateRut

# Create your models here.

ESTADOS = (
    ('pendiente', 'Pendiente'),
    ('Entregado', 'Entregado'),
)

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=13, unique=True, validators=[ValidateRut])
    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=30, default='N/A', unique=True)
    estado = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre
        

class Prestamo(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="Ingreso")
    descripcion = models.CharField(max_length=100, blank=True)
    ubicacion = models.CharField(max_length=50)
    cantidad = models.IntegerField(validators=[ValidateMayorCero])
    estado = models.CharField(max_length=20, default='pendiente', choices=ESTADOS)
    codigo = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.id, self.id_user.nombre)


    def save(self, *args, **kwargs):

        cod = not self.pk
        super().save(*args, **kwargs)

        if cod:
            self.codigo = str(self.id)+'000'
            kwargs['force_insert'] = False
            super().save(*args, **kwargs)

class Ingreso(models.Model):
    id_pres = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[ValidateMayorCero],null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)