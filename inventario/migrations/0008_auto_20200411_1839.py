# Generated by Django 2.2.10 on 2020-04-11 22:39

from django.db import migrations, models
import inventario.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_merge_20200309_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stock_min',
            field=models.IntegerField(default=0, validators=[inventario.validators.ValidateNumeroPositivo]),
        ),
    ]
