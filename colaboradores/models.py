from django.db import models


class Colaborador(models.Model):
    nombre = models.CharField(max_length=250)
    