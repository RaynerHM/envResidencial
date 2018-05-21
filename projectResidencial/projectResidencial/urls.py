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
from Residencial import views
# from Residencial import GenerarPDF
from django.contrib.auth.views import login, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear-cuenta/', views.Registrar, name='crear-cuenta'),
    path('cambiar-clave/', views.CambiarClave, name='clave'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('', views.EstadosCuenta, name='estado'),
    path('estado-de-cuenta/', views.EstadosCuenta, name='estado'),
    path('registrar-pagos/', views.RegistrarPagos, name='pagos'),
    path('reporte/estadoDeCuenta/pdf/', views.ReportePersonasPDF.as_view(), name='reporte'),
    path('correo/', views.EnviarCorreo, name='correo'),


]
