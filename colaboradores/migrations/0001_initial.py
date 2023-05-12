# Generated by Django 4.1.7 on 2023-05-04 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farmacias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('farmacia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmacias.farmacia')),
            ],
        ),
    ]
