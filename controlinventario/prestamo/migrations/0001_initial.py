# Generated by Django 2.2.1 on 2019-11-07 04:46

from django.db import migrations, models
import django.db.models.deletion
import prestamo.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, null=True, validators=[prestamo.validators.ValidateMayorCero])),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rut', models.CharField(max_length=13, unique=True, validators=[prestamo.validators.ValidateRut])),
                ('nombre', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=10)),
                ('email', models.CharField(default='N/A', max_length=30, unique=True)),
                ('estado', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(blank=True, max_length=100)),
                ('ubicacion', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField(validators=[prestamo.validators.ValidateMayorCero])),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('Entregado', 'Entregado')], default='pendiente', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prestamo.Usuario')),
                ('productos', models.ManyToManyField(through='prestamo.Ingreso', to='inventario.Producto')),
            ],
        ),
        migrations.AddField(
            model_name='ingreso',
            name='id_pres',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prestamo.Prestamo'),
        ),
        migrations.AddField(
            model_name='ingreso',
            name='id_prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto'),
        ),
    ]