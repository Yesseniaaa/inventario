# Generated by Django 2.2.10 on 2020-03-16 14:02

import adquisiciones.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_merge_20200309_2140'),
        ('adquisiciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MermaM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(validators=[adquisiciones.validators.ValidateMayorCero])),
                ('observaciones', models.TextField(max_length=200)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Devolucion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(validators=[adquisiciones.validators.ValidateMayorCero])),
                ('fecha', models.DateField()),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto')),
            ],
        ),
    ]