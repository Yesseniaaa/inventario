# Generated by Django 2.2.1 on 2020-02-19 00:59

from django.db import migrations, models
import django.db.models.deletion
import salidas.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rut', models.CharField(max_length=15, unique=True, validators=[salidas.validators.ValidateRut])),
                ('nombres', models.CharField(max_length=40)),
                ('paterno', models.CharField(max_length=40)),
                ('materno', models.CharField(max_length=40)),
                ('mail', models.CharField(max_length=50, unique=True)),
                ('telefono', models.CharField(max_length=9, validators=[salidas.validators.ValidarTelefono])),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pre_prod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recinto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=100)),
                ('estado', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sal_prod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('id_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Salida',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('total', models.IntegerField()),
                ('id_funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salidas.Funcionario')),
                ('id_recinto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salidas.Recinto')),
                ('productos', models.ManyToManyField(through='salidas.Sal_prod', to='inventario.Producto')),
            ],
        ),
        migrations.AddField(
            model_name='sal_prod',
            name='id_salida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salidas.Salida'),
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('total', models.IntegerField()),
                ('devolucion', models.DateField()),
                ('id_funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salidas.Funcionario')),
                ('id_recinto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salidas.Recinto')),
                ('productos', models.ManyToManyField(through='salidas.Pre_prod', to='inventario.Producto')),
            ],
        ),
        migrations.AddField(
            model_name='pre_prod',
            name='id_prestamo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salidas.Prestamo'),
        ),
        migrations.AddField(
            model_name='pre_prod',
            name='id_prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='id_recinto',
            field=models.ManyToManyField(to='salidas.Recinto'),
        ),
    ]
