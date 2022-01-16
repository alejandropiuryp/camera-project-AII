#encoding:utf-8
from main.models import Camara, Categoria, Objetivo, Montura, Motor, Paquete
import urllib.request
from bs4 import BeautifulSoup
import re
from whoosh.fields import Schema, NUMERIC, TEXT, STORED, KEYWORD
import os, shutil
from whoosh.index import create_in, open_dir
from whoosh.analysis import StandardAnalyzer, KeywordAnalyzer

URL_MIRRORLESS = "https://store.canon.es/camaras-compactas-de-sistema/p/"
URL_DSLR = "https://store.canon.es/camaras-reflex/p/"

def populateDB_canon():
    print("-------------Cargando Camaras Canon-------------")
    Categoria.objects.all().delete()
    Motor.objects.all().delete()
    Montura.objects.all().delete()
    Objetivo.objects.all().delete()
    Camara.objects.all().delete()
    Paquete.objects.all().delete()

    print("-------------Cargando Camaras Canon Mirrorless-------------")
    populate_camaras(URL_MIRRORLESS,"MR")

    print("-------------Cargando Camaras Canon DSRL-------------")
    populate_camaras(URL_DSLR,"DSLR")

def populate_camaras(url,tipo):
    for pag in range(1,3):
        f = urllib.request.urlopen(url + str(pag))
        s = BeautifulSoup(f,"lxml")
        camaras = s.find_all("div",class_="layout-item-container item-count-1")
        for camara in camaras:
            url_camara = camara.find("a",class_="product-tile-list-header--anchor no-underline")
            f_camara = urllib.request.urlopen("https://store.canon.es/" + url_camara['href'])
            s_camara = BeautifulSoup(f_camara, "lxml")
            nombre = s_camara.find("span",class_="pt_bold").string.strip()
            if nombre.startswith(("Cámara", "Cuerpo","Canon")) == True:
                nombre_camara = nombre
                print(nombre_camara)

                #Foto
                imagen = "https:/" + camara.find("div",class_="product-image").find("img")["data-src"].split(", ")[1][1:-3]
                print(imagen)

                #Precio
                spans = camara.find("span",class_="price-amount").find_all("span")
                precio = ""
                for span in spans:
                    precio += span.string.strip()

                url_detalles = s_camara.find("div",id="1600009p")
                if url_detalles == None:
                    sensor,iso,procesador = extraer_detalles(s_camara)
                else:
                    url_detalles = url_detalles.find("p",class_="header-5 mom-tab--heading").a["href"]
                    f_detalles = urllib.request.urlopen(url_detalles)
                    s_detalles = BeautifulSoup(f_detalles, "lxml")
                    if s_detalles.find("section",class_="flex-global-style__old-template breadcrumbs__container"):
                        #SENSOR
                        tipo_sensor = s_detalles.find("div",string="Tipo")
                        if tipo_sensor == None:
                            sensor = s_detalles.find("h4",string="Tipo").find_next_sibling("div").p.string.strip()
                        else:
                            sensor = tipo_sensor.find_next_sibling("div").div.string.strip()

                        #PROCESADOR
                        tipo_procesador = s_detalles.find("h3",string="Procesador de imagen").find_next_sibling("ul")
                        if tipo_procesador == None:
                            procesador = s_detalles.find("h3",string="Procesador de imagen").find_next_sibling("div").div.div.p.string.strip()
                        else:
                            procesador = tipo_procesador.find("div",string="Tipo").find_next_sibling("div").div.string.strip()

                        #ISO
                        titulo_iso = s_detalles.find("div",string="ISO")
                        if titulo_iso == None:
                            titulo_iso = s_detalles.find("h4",string="Sensibilidad ISO")
                            titulo_iso2 = s_detalles.find("h4",string="Sensibilidad ISO equivalente")
                            if titulo_iso:
                                iso = ".".join(titulo_iso.find_next_sibling("div").p.stripped_strings)
                            elif titulo_iso2:
                                iso = ".".join(titulo_iso2.find_next_sibling("div").p.stripped_strings)
                            else:
                                lis = s_detalles.find("h3",string="Control de la exposición").find_next_sibling("ul").find_all("li")
                                iso = ".".join(lis[len(lis) - 1].find("div",class_="product-specification-detail__list-value canon-paragraph--big").stripped_strings)
                        else:
                            iso = ".".join(titulo_iso.find_next_sibling("div").div.stripped_strings)
                    else:
                        sensor = "Desconocido"
                        iso = "Desconocido"
                        procesador = "Desconocido"

                print(sensor)
                print(iso)
                print(procesador)
                #Tipo
                tipo = Categoria.objects.get_or_create(tipo=tipo)[0]
                print(tipo)
                #Camara
                camara_objeto = Camara.objects.get_or_create(nombre=nombre_camara,sensor=sensor,iso=iso,procesador=procesador,foto=imagen,tipo=tipo)[0]

                complementos = camara.find_all("span",class_="pt_red")

                if complementos:
                    camara_objeto.precio = "Desconocido"
                    camara_objeto.save()
                    print("Precio desconocido")
                    print("-------------Cargando Objetivo-------------")
                    #Objetivo
                    objetivos = []
                    for complemento in complementos:
                        nombre_campo = complemento.next_sibling.string.strip()
                        sub_division = re.split(" y | o ",nombre_campo)
                        print(sub_division)
                        if len(sub_division) > 1:
                            for division in sub_division:
                                objetivo = crear_objetivo(division)
                                if objetivo:
                                    objetivos.append(objetivo)
                        else:
                            objetivo = crear_objetivo(nombre_campo)
                            if objetivo:
                                objetivos.append(objetivo)
                    print("-------------Cargando Paquete-------------")
                    paquete = Paquete.objects.create(camara=camara_objeto,precio=precio)
                    paquete.objetivos.set(objetivos)

                else:
                    camara_objeto.precio = precio
                    camara_objeto.save()
                    print(precio)

                print("--------------------------")

def crear_objetivo(objetivo_string):
    if objetivo_string.startswith(("objetivo","Objetivo")):
        propiedades_objetivo = objetivo_string.split()
        print(propiedades_objetivo)
        montura = Montura.objects.get_or_create(tipo=propiedades_objetivo[1].strip())[0]
        print(montura)
        distancia_focal = propiedades_objetivo[2].strip()
        print(distancia_focal)
        
        if "IS" in propiedades_objetivo:
            estabilizador = "Si"
        else:
            estabilizador = "No"

        print(estabilizador)
        
        motor_enfoque = ""
        opts = ['USM','STM','MACRO']
        for opt in opts:
            if opt in propiedades_objetivo:
                motor_enfoque = Motor.objects.get_or_create(tipo=opt)[0]
                break

        if motor_enfoque == "":
            motor_enfoque = Motor.objects.get_or_create(tipo="MANUAL")[0]
        print(motor_enfoque)

        apertura_regex = re.search(r"f+\/+\d+(.\d)?-+\d+(.\d)",objetivo_string)
        if apertura_regex:
            apertura = apertura_regex[0]
        else:
            apertura = "Desconocido"
        print(apertura)   
        
        objetivo = Objetivo.objects.get_or_create(montura=montura,distancia_focal=distancia_focal,apertura=apertura,estabilizador=estabilizador,motor_enfoque=motor_enfoque)[0]
        return objetivo
    elif objetivo_string.startswith("E"):
        propiedades_objetivo = objetivo_string.split()
        montura = Montura.objects.get_or_create(tipo=propiedades_objetivo[0].strip())[0]
        print(montura)
        distancia_focal = propiedades_objetivo[1].strip()
        print(distancia_focal)
        
        if "IS" in propiedades_objetivo:
            estabilizador = "Sí"
        else:
            estabilizador = "No"

        print(estabilizador)
        
        opts = ['USM','STM','MACRO']
        for opt in opts:
            if opt in propiedades_objetivo:
                motor_enfoque = Motor.objects.get_or_create(tipo=opt)[0]
            else:
                motor_enfoque = Motor.objects.get_or_create(tipo="MANUAL")[0]
        print(motor_enfoque)

        apertura_regex = re.search(r"f+\/+\d+(.\d)?-+\d+(.\d)",objetivo_string)
        if apertura_regex:
            apertura = apertura_regex[0]
        else:
            apertura = "Desconocido"
        print(apertura)   
        
        objetivo = Objetivo.objects.get_or_create(montura=montura,distancia_focal=distancia_focal,apertura=apertura,estabilizador=estabilizador,motor_enfoque=motor_enfoque)[0]

        return objetivo
    else:
        return None


def extraer_detalles(pag_camara):
    if pag_camara.find("div",class_="product-specs"):
        sensor = pag_camara.find("th",string="TIPO DE SENSOR DE IMAGEN").find_next_sibling("td").string.strip()
        iso = pag_camara.find("th",string="SENSIBILIDAD ISO").find_next_sibling("td").string.strip()
        procesador = pag_camara.find("th",string="Tipo").find_next_sibling("td").string.strip()
    else:
        sensor = "Desconocido"
        iso = "Desconocido"
        procesador = "Desconocido"
    return (sensor,iso,procesador)

def populateWhoosh():
    schemCamaras = Schema(id=NUMERIC(stored=True),nombre=TEXT(stored=True,analyzer=StandardAnalyzer(minsize=1)),sensor=TEXT(stored=True, analyzer=KeywordAnalyzer()),iso=TEXT(stored=True,analyzer=KeywordAnalyzer()),
    procesador=TEXT(stored=True, analyzer=KeywordAnalyzer()),precio=TEXT(stored=True),foto=STORED(),tipo=KEYWORD(stored=True,commas=True))

    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")

    ix = create_in("Index",schema=schemCamaras)
    writer = ix.writer()
    camaras = Camara.objects.all()
    for camara in camaras:
        writer.add_document(id=camara.id,nombre=camara.nombre,sensor=camara.sensor,
        iso=camara.iso,procesador=camara.procesador,precio=camara.precio[:-1],foto=camara.foto,tipo=camara.tipo.get_tipo_display())
    writer.commit()
