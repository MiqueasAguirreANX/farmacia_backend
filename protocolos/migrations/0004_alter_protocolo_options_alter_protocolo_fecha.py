# Generated by Django 4.1.7 on 2023-06-21 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocolos', '0003_alter_protocolo_fecha_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='protocolo',
            options={'ordering': ['-fecha']},
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
