from django.contrib import admin
from main.models import Camara, Categoria, Montura, Motor, Objetivo, Paquete

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Motor)
admin.site.register(Montura)
admin.site.register(Objetivo)
admin.site.register(Camara)
admin.site.register(Paquete)