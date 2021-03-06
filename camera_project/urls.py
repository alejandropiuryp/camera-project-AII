"""canon_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from main import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',  include("django.contrib.auth.urls")),
    path('',views.inicio, name='inicio'),
    path('cargar/', views.cargar, name='cargarBD'),
    path('camaras/',views.listar_camaras, name='camaras'),
    path('camara/<int:id>',views.detalle_camara, name='camara'),
    path('paquetes/',views.listar_paquetes, name='paquetes'),
    path('buscarCamaras/',views.buscar_camaras),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

