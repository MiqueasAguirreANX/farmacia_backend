# Generated by Django 4.1.7 on 2023-03-19 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.IntegerField(blank=True, default=0, null=True)),
                ('nombre', models.CharField(blank=True, max_length=250, null=True)),
                ('apellido', models.CharField(blank=True, max_length=250, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('celular', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.EmailField(blank=True, max_length=250, null=True)),
                ('domicilio', models.CharField(blank=True, max_length=250, null=True)),
                ('entre_calles', models.CharField(blank=True, max_length=250, null=True)),
                ('codigo_postal', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]