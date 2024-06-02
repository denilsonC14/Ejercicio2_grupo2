from django.db import models # es una librería que nos permite trabajar con bases de datos

class Producto(models.Model): # se crea una clase que hereda de models.Model
    nombre = models.CharField(max_length=100) # se crea un atributo nombre de tipo CharField
    precio = models.DecimalField(max_digits=10, decimal_places=2) # se crea un atributo precio de tipo DecimalField
    cantidad = models.IntegerField() # se crea un atributo cantidad de tipo IntegerField

    def __str__(self): #  se manipula o se mejora la representación de un objeto en string
        return self.nombre
