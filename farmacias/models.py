from django.db import models
from django.contrib.auth.models import User


class Farmacia(models.Model):
    logo = models.ImageField(default='default.jpeg', upload_to='logos')
    nombre = models.CharField(max_length=255, default="farmacia")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
