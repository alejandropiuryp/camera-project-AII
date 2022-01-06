#encoding:utf-8
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Categoria(models.Model):
    MIRRORLESS = 'MR'
    DIGITAL = 'DSLR'
    COMPACTAS = 'CC'
    
    TIPOS_CAMARA =  [
        (MIRRORLESS,'Mirrorless'),
        (DIGITAL, 'DSRL'),
        (COMPACTAS, 'Compacta')
    ]

    tipo = models.CharField(max_length=4,choices=TIPOS_CAMARA)

    def __str__(self):
        return self.tipo


class Camara(models.Model):
    nombre = models.TextField()
    sensor = models.TextField()
    iso = models.TextField()
    procesador = models.TextField()
    precio = models.TextField()
    foto = models.ImageField()

    tipo = models.ForeignKey(Categoria,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.nombre


