#encoding:utf-8
from django import forms
from main.models import Categoria


class Buscar_camara(forms.Form):
    tipo = forms.ModelChoiceField(label="Seleccione el tipo", queryset=Categoria.objects.all(),required=True)
    consulta = forms.CharField(label="Nombre o Precio", required=True)