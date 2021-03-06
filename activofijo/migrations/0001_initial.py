# Generated by Django 2.2.1 on 2020-02-19 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('salidas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activofijo',
            fields=[
                ('id_activo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('cod_barra', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('estado', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id_funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salidas.Funcionario')),
                ('id_recinto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salidas.Recinto')),
            ],
        ),
    ]
