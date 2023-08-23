"""farmacia_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from rest_framework import permissions
from farmacias.views import CustomAuthToken

def index(request):
    return render(request, 'index.html', {})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path("api/clientes/", include("clientes.urls")),
    path("api/colaboradores/", include("colaboradores.urls")),
    path("api/observaciones/", include("observaciones.urls")),
    path("api/protocolos/", include("protocolos.urls")),
    path("api/servicios/", include("servicios.urls")),
    path("api/farmacias/", include("farmacias.urls")),
    path("api/auth/", CustomAuthToken.as_view(), name="auth"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
