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


class OrdenAdq(models.Model):
    id = models.AutoField(primary_key=True)
    id_prov = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    factura = models.IntegerField(validators=[ValidateMayorCero])
    fecha_factura = models.DateField()
    productos = models.ManyToManyField(Producto, through="Ingreso")
    precio_compra = models.IntegerField(validators=[ValidateMayorCero])
    cantidad = models.IntegerField(validators=[ValidateMayorCero])
    estado = models.CharField(max_length=20, default='pendiente', choices=ESTADOS)
    codigo = models.CharField(max_length=40, unique=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.id, self.id_prov.nombre)

    def save(self, *args, **kwargs):
        cod = not self.pk
        super().save(*args, **kwargs)

        if cod:
            self.codigo = str(self.id) + '000'
            kwargs['force_insert'] = False
            super().save(*args, **kwargs)


class Ingreso(models.Model):
    id_adq = models.ForeignKey(OrdenAdq, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_compra = models.IntegerField(validators=[ValidateMayorCero])
    cantidad = models.IntegerField(validators=[ValidateMayorCero], null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class MermaM(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[ValidateMayorCero])
    observaciones = models.TextField(max_length=200)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class Devolucion(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[ValidateMayorCero])
    fecha = models.DateField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
