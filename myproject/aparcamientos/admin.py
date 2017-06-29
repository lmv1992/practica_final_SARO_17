from django.contrib import admin
from aparcamientos.models import Aparcamiento,PaginaUsuario,Comentario, AparcamientoSeleccionado


# Register your models here.

admin.site.register(Aparcamiento)
admin.site.register(PaginaUsuario)
admin.site.register(Comentario)
admin.site.register(AparcamientoSeleccionado)
