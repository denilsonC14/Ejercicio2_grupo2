from django.contrib import admin
from .models import Producto # importamos el modelo Producto

admin.site.register(Producto) # registramos el modelo Producto en el admin que no es tan necesario pero es una buena practica
