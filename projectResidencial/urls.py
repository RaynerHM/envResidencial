"""projectResidencial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from AppResidencial import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear_cuenta/', views.registrar_usuario, name='crear_cuenta'),
    path('cambiar_clave_ajax/', views.cambiar_clave_ajax, name='claveAjax'),
    path('cambiar_clave/', views.cambiar_clave, name='clave'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.estados_cuenta, name='estado'),
    # path('estado-de-cuenta/', views.estados_cuenta, name='estado'),
    path('registrar_pagos/', views.registrar_pagos, name='pagos'),
    path('sugerencias_ajax/', views.sugerencias_ajax, name='sugerencias_ajax'),
    path('cargar_nombres_ajax/', views.cargar_nombres_ajax, name='cargar_nombres_ajax'),

    path('reporte/pdf/estado_de_cuenta/',
         views.reporte_estado_de_cuenta_personal.as_view(), name='reporte'),
    path('correo/', views.EnviarCorreo, name='correo'),
    path('buscar_deuda_ajax/', views.buscar_deuda_ajax, name='buscar_deuda_ajax'),
    path('guardar_ajax/', views.guardar_ajax, name='guardar_ajax'),
    path('configurar_usuarios/', views.configurar_usuarios,
         name='usuarios'),
]
admin.site.site_header = 'Admin - Residencial Brisa Fresca'

