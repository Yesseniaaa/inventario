# Generated by Django 2.2.10 on 2020-03-16 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salidas', '0004_merge_20200309_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pre_prod',
            name='precio',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sal_prod',
            name='precio',
            field=models.IntegerField(null=True),
        ),
    ]
