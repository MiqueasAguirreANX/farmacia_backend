# Generated by Django 4.1.7 on 2023-03-25 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('colaboradores', '0001_initial'),
        ('clientes', '0001_initial'),
        ('servicios', '0001_initial'),
        ('protocolos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolo',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='colaborador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='colaboradores.colaborador'),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='servicio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servicios.servicio'),
        ),
    ]