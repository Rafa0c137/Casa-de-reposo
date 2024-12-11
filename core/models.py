# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()  # Asegúrate de que esto esté definido

    def __str__(self):
        return self.nombre
