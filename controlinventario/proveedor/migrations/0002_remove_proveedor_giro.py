# Generated by Django 2.2.1 on 2019-11-07 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='giro',
        ),
    ]
