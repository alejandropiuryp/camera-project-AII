#encoding:utf-8
from main.models import Camara, Categoria
import urllib.request
from bs4 import BeautifulSoup
import re

def populateDB_canon():
    print("-------------Cargando Camaras Canon-------------")
    Categoria.objects.all().delete()
    Camara.objects.all().delete()

    populate_canon_mirrorless()

def populate_canon_mirrorless():
    print("-------------Cargando Camaras Canon Mirrorless-------------")
    for pag in range(1,3):
        f = urllib.request.urlopen("https://store.canon.es/camaras-compactas-de-sistema/p/"+str(pag))
        s = BeautifulSoup(f,"lxml")
        camaras = s.find_all("div",class_="layout-item-container item-count-1")
        for camara in camaras:
            print("--------------------------")
            url = camara.find("a",class_="product-tile-list-header--anchor no-underline")
            f_camara = urllib.request.urlopen("https://store.canon.es/" + url['href'])
            s_camara = BeautifulSoup(f_camara, "lxml")
            nombre = s_camara.find("span",class_="pt_bold").string.strip()
            if nombre.startswith(("Cámara", "Cuerpo")) == True:
                print(nombre)

                #Precio
                spans = camara.find("span",class_="price-amount").find_all("span")
                precio = ""

                #Foto
                imagen = camara.find("div",class_="product-image").find("img")["data-src"].split(", ")[1][1:-3]
                print(imagen)

                for span in spans:
                    precio += span.string.strip()
                print(precio)
                url_detalles = s_camara.find("div",id="1600009p")
                if url_detalles == None:
                    sensor = "Desconocido"
                    iso = "Desconocido"
                    procesador = "Desconocido"
                else:
                    url_detalles = url_detalles.find("p",class_="header-5 mom-tab--heading").a["href"]
                    f_detalles = urllib.request.urlopen(url_detalles)
                    s_detalles = BeautifulSoup(f_detalles, "lxml")

                    #SENSOR
                    tipo_sensor = s_detalles.find("div",string="Tipo")
                    if tipo_sensor == None:
                        sensor = s_detalles.find("h4",string="Tipo").find_next_sibling("div").p.string.strip()
                    else:
                        sensor = tipo_sensor.find_next_sibling("div").div.string.strip()
                    print(sensor)

                    #PROCESADOR
                    tipo_procesador = s_detalles.find("h3",string="Procesador de imagen").find_next_sibling("ul")
                    if tipo_procesador == None:
                        procesador = s_detalles.find("h3",string="Procesador de imagen").find_next_sibling("div").div.div.p.string.strip()
                    else:
                        procesador = tipo_procesador.find("div",string="Tipo").find_next_sibling("div").div.string.strip()
                    print(procesador)

                    #ISO
                    titulo_iso = s_detalles.find("div",string="ISO")
                    if titulo_iso == None:
                        titulo_iso = s_detalles.find("h4",string="Sensibilidad ISO")
                        if titulo_iso == None:
                            lis = s_detalles.find("h3",string="Control de la exposición").find_next_sibling("ul").find_all("li")
                            iso = ".".join(lis[len(lis) - 1].find("div",class_="product-specification-detail__list-value canon-paragraph--big").stripped_strings)
                        else:
                            iso = ".".join(titulo_iso.find_next_sibling("div").p.stripped_strings)
                    else:
                        iso = ".".join(titulo_iso.find_next_sibling("div").div.stripped_strings)
                    print(iso)
                #Tipo
                tipo = Categoria.objects.get_or_create(tipo="MR")[0]
                #Camara
                camara = Camara.objects.create(nombre=nombre,sensor=sensor,iso=iso,procesador=procesador,precio=precio,foto=imagen,tipo=tipo)




