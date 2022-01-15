#encoding:utf-8
from django.shortcuts import render,redirect,get_object_or_404
from main import populate
from main.models import Camara, Categoria, Objetivo, Paquete
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from main.forms import Buscar_camara

# Create your views here.
def inicio(request):
    return render(request,'inicio.html')

@login_required
def cargar(request):
    logout(request)
    if request.method=='POST':
        if 'Aceptar' in request.POST:  
            populate.populateDB_canon()    
            populate.populateWhoosh()
            num_camaras = Camara.objects.count()
            num_objetivos = Objetivo.objects.count()
            num_paquetes = Paquete.objects.count()

            mensaje="Se han almacenado: " + str(num_camaras) +" camaras, " + str(num_objetivos) +" objetivos, " + str(num_paquetes) +" paquetes"
            return render(request, 'cargar.html', {'mensaje':mensaje})
        else:
            return redirect("/")
    return render(request,'confirmacion.html')

def listar_camaras(request):
    camaras =Camara.objects.exclude(precio="Desconocido")
    return render(request, 'camaras.html', {'camaras':camaras})

def detalle_camara(request, id):
    camara=get_object_or_404(Camara,pk=id)
    print(camara.tipo.get_tipo_display())
    return render(request, 'camara.html', {'camara':camara})

def listar_paquetes(request):
    paquetes=Paquete.objects.all()
    print(paquetes[0].camara)
    return render(request, 'paquetes.html', {'paquetes':paquetes})


def buscar_camaras(request):
    populate.populateWhoosh()
    form = Buscar_camara()
    lista_camaras = []
    consulta = ""

    if request.method=='POST':
        form = Buscar_camara(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            consulta = form.cleaned_data['consulta']
            directorio = 'Index'
            ix = open_dir('Index')
            with ix.searcher() as searcher:
                query = MultifieldParser(["nombre","tipo","procesador","sensor","iso"], ix.schema).parse(consulta + " " + tipo.get_tipo_display())
                camaras = searcher.search(query)
                for camara in camaras:
                    camara_obj = Camara.objects.get(pk=camara['id'])
                    if camara_obj not in lista_camaras:
                        lista_camaras.append(camara_obj)
            return render(request,'buscador.html',{'formulario':form,'camaras':lista_camaras,'tipo':consulta})
    return render(request,'buscador.html',{'formulario':form,'camaras':lista_camaras,'tipo':consulta})

def handler_404(request,exception):
    return render(request,"404.html")

