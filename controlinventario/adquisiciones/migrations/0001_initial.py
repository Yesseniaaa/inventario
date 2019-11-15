# Generated by Django 2.2.1 on 2019-11-14 23:55

import adquisiciones.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0003_remove_producto_ubicacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_compra', models.IntegerField(validators=[adquisiciones.validators.ValidateMayorCero])),
                ('cantidad', models.IntegerField(blank=True, null=True, validators=[adquisiciones.validators.ValidateMayorCero])),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rut', models.CharField(max_length=13, unique=True, validators=[adquisiciones.validators.ValidateRut])),
                ('nombre', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=10)),
                ('email', models.CharField(default='N/A', max_length=30, unique=True)),
                ('estado', models.BooleanField(default=True)),
                ('nom_cont', models.CharField(max_length=20)),
                ('giro', models.CharField(max_length=100)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenAdq',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('precio_compra', models.IntegerField(validators=[adquisiciones.validators.ValidateMayorCero])),
                ('cantidad', models.IntegerField(validators=[adquisiciones.validators.ValidateMayorCero])),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')], default='pendiente', max_length=20)),
                ('codigo', models.CharField(max_length=40, unique=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('id_prov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adquisiciones.Proveedor')),
                ('productos', models.ManyToManyField(through='adquisiciones.Ingreso', to='inventario.Producto')),
            ],
        ),
        migrations.AddField(
            model_name='ingreso',
            name='id_adq',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adquisiciones.OrdenAdq'),
        ),
        migrations.AddField(
            model_name='ingreso',
            name='id_prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto'),
        ),
    ]