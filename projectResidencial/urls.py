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
    path('crear-cuenta/', views.RegistrarUsuario, name='crear-cuenta'),
    path('cambiarclaveAjax/', views.CambiarClaveAjax, name='claveAjax'),
    path('cambiarClave/', views.CambiarClave, name='clave'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('', views.EstadosCuenta, name='estado'),
    # path('estado-de-cuenta/', views.EstadosCuenta, name='estado'),
    path('registrar-pagos/', views.RegistrarPagos, name='pagos'),
    path('sugerenciasAjax/', views.SugerenciasAjax, name='sugerenciasAjax'),
    path('CargarNombresAjax/', views.CargarNombresAjax, name='CargarNombresAjax'),

    path('reporte/estadoDeCuenta/pdf/',
         views.ReportePersonasPDF.as_view(), name='reporte'),
    path('correo/', views.EnviarCorreo, name='correo'),
    path('ajaxbuscardeuda/', views.AjaxBuscarDeuda, name='ajaxbuscardeuda'),
    path('ajaxguardar/', views.AjaxGuardar, name='ajaxguardar'),
    path('usuarios/', views.ConfigurarUsuarios,
         name='usuarios'),
]
admin.site.site_header = 'Admin - Residencial Brisa Fresca'
