from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Aparcamiento(models.Model):
    nombre = models.TextField(default="")
    descripcion = models.TextField(default="")
    accessibilidad = models.IntegerField(default="")
    url = models.TextField(default="")
    barrio = models.TextField(default="")
    distrito = models.TextField(default="")
    latitud = models.FloatField(default=0)
    longitud = models.FloatField(default=0)
    cuantidad_likes = models.IntegerField(default = 0)
    numero_comentarios = models.IntegerField(default = 0)
    def __str__(self):
        return self.nombre

class PaginaUsuario(models.Model):
    usuario = models.ForeignKey(User)
    titulo = models.TextField(default="Página de ususario")
    color = models.CharField(default="#e9dede", max_length=32)
    tamanho = models.IntegerField(default=12)
    def __str__(self):
        return self.usuario

class Comentario(models.Model):
    anotacion = models.TextField(default="")
    fecha = models.DateField(auto_now_add=True)
    aparcamiento = models.ForeignKey(Aparcamiento, default="")
    usuario = models.ForeignKey(User)
    def __str__(self):
        return self.aparcamiento

class AparcamientoSeleccionado(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    usuario = models.ForeignKey(User)
    fecha = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.aparcamiento
