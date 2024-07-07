from django.db import models

from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('normal', 'Usuario Normal'),
    )

    rol = models.CharField(max_length=7, choices=ROLES, default='normal')


class Evento(models.Model):
    nombre = models.CharField(max_length=150)
    descripción = models.TextField()
    fecha_de_inicio = models.DateField()
    fecha_fin = models.DateField()
    ubicación = models.CharField(max_length=255)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cupos = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)
    inscritos = models.ManyToManyField(Usuario, related_name='eventos_inscritos', blank=True)

    def __str__(self):
        return self.nombre