#encoding:utf-8
from django.shortcuts import render
from main import populateDB

# Create your views here.
def inicio(request):
    return render(request,'inicio.html')

def cargar(request):
    populateDB.populateDB_canon()
    return render(request,'cargar.html')
