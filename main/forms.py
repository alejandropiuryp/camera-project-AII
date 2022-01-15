#encoding:utf-8
from django import forms
from main.models import Categoria


class Buscar_camara(forms.Form):
    tipo = forms.ModelChoiceField(label="Seleccione el tipo", queryset=Categoria.objects.all(),required=True)
    nombre = forms.CharField(label="Nombre", required=False)
    procesador = forms.CharField(label="Procesador", required=False)
    iso = forms.CharField(label="ISO", required=False)
    sensor = forms.CharField(label="Sensor", required=False)