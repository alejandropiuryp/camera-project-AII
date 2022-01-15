#encoding:utf-8
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

# Create your models here.
class Categoria(models.Model):
    MIRRORLESS = 'MR'
    DIGITAL = 'DSLR'
    
    TIPOS_CAMARA =  [
        (MIRRORLESS,'Mirrorless'),
        (DIGITAL, 'DSRL'),
    ]

    tipo = models.CharField(max_length=4,choices=TIPOS_CAMARA)

    def __str__(self):
        return self.tipo


class Motor(models.Model):
    TIPOS_MOTOR =  [
        ('USM','USM'),
        ('STM', 'STM'),
        ('MACRO', 'MACRO'),
        ('MANUAL','MANUAL')
    ]

    tipo = models.CharField(max_length=6,choices=TIPOS_MOTOR)

    def __str__(self):
        return self.tipo

class Montura(models.Model):
    TIPOS_MONTURA =  [
        ('EF','EF'),
        ('EF-S', 'EF-S'),
        ('EF-M', 'EF-M')
    ]

    tipo = models.CharField(max_length=4,choices=TIPOS_MONTURA)

    def __str__(self):
        return self.tipo


class Objetivo(models.Model):
    montura = models.ForeignKey(Montura,on_delete=SET_NULL,null=True)
    distancia_focal = models.TextField()
    apertura = models.TextField()
    estabilizador = models.CharField(max_length=2)
    motor_enfoque = models.ForeignKey(Motor,on_delete=SET_NULL,null=True)




class Camara(models.Model):
    nombre = models.TextField()
    sensor = models.TextField()
    iso = models.TextField()
    procesador = models.TextField()
    precio = models.TextField()
    foto = models.ImageField()

    tipo = models.ForeignKey(Categoria,on_delete=SET_NULL,null=True)

    def __str__(self):
        return self.nombre

class Paquete(models.Model):
    camara = models.ForeignKey(Camara,on_delete=CASCADE)
    objetivos = models.ManyToManyField(Objetivo)
    precio = models.TextField(null=True)

    def __str__(self):
        return self.precio
