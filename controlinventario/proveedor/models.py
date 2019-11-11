from django.db import models
from inventario.models import Producto, RegistroTemporalProducto
from .validators import ValidateMayorCero, ValidateRut


ESTADOS = (
    ('pendiente', 'Pendiente'),
    ('pagado', 'Pagado'),
)

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=13, unique=True, validators=[ValidateRut])
    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=30, default='N/A', unique=True)
    estado = models.BooleanField(default=True)
    nom_cont = models.CharField(max_length=20)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


    def __str__(self):
        return self.nombre