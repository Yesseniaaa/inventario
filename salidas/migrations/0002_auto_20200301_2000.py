# Generated by Django 2.2.1 on 2020-03-01 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salidas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pre_prod',
            name='precio',
            field=models.IntegerField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sal_prod',
            name='precio',
            field=models.IntegerField(max_length=50),
        ),
    ]
