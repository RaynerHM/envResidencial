from django.shortcuts import render

from .models import Residente, Apartamento, Pago, Ajuste

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.views.generic import View

# import datetime
import time
from dateutil.relativedelta import *

from .pdf import render_pdf


def Login(request):
	mensaje = ''
	if request.method == 'POST':
		v_usuario = request.POST.get('username')
		v_clave = request.POST.get('password')

		usuario = auth.authenticate(username=v_usuario, password=v_clave)
		if usuario is not None:
			auth.login(request, usuario)
			return redirect(EstadosCuenta)
		else:
			mensaje = 'Usuario o clave incorrecto'
	return render(request, 'login.html', {'mensaje': mensaje})


@login_required(login_url='/login/')
def Logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login")


def Registrar(request):
	if request.method == 'POST':
		v_nombre = request.POST.get('nombre')
		v_apellido = request.POST.get('apellido')
		v_correo = request.POST.get("correo")
		v_no_apartamento = request.POST.get("apartamento")
		v_edificio = request.POST.get("edificio")
		v_telefono = request.POST.get("telefono")
		v_cedula = request.POST.get("cedula")
		v_clave = request.POST.get("clave")

		if (v_nombre != '' and v_apellido != '' and v_correo != ''
			and v_telefono != '' and   v_cedula != ''  and  v_clave!= ''):

		#Crear registro del Residente
			residente = Residente.objects.create(
											nombre=(v_nombre +
											' ' + v_apellido),
											no_apartamento=v_no_apartamento,
											edificio=v_edificio,
											correo=v_correo,
											telefono=v_telefono,
											cedula=v_cedula,
											clave=v_clave
											)

		#Crear usuario del Residente, para poder iniciar sesion
			usuario = User.objects.create_user(
											username=v_correo,
											password=v_clave,
											first_name=v_nombre,
											last_name=v_apellido,
											email=v_correo
											)
			is_active = True
			usuario.is_staff = True
			usuario.save()

			return render(request, "felicidades.html",
			{'nombre': v_nombre, 'correo': v_correo})
		else:
			return render(request, "registro_residente.html")
	return render(request, "registro_residente.html")


# ------------ Pendiente por terminar ------------
@login_required(login_url='/login/')
def CambiarClave(request):
	mensaje = ''
	if request.method == 'POST':
		v_clave_Vieja = request.POST.get("pass-last")
		v_clave_Nueva = request.POST.get("pass-new")

		clave = User.objects.get(username=request.user)
		if clave == v_clave_Vieja:
			clave.set_password(v_clave_Nueva)
			clave.save()

			mensaje = "Clave cambiada exitosamente"
		else:
			mensaje = "Fallo al cambiar la clave"
		return render(request, "password.html", {'mensaje': mensaje})
	return render(request, "password.html")


@login_required(login_url='/login/')
def Sesion(request):
	return render(request, "sesion.html")


@login_required(login_url='/login/')
def EstadosCuenta(request):
	usuario= request.user.get_full_name()

	ajuste = Ajuste.objects.all()

	pago = Pago.objects.all().filter(propietario__nombre=usuario)
	deuda=0
	deuda_pendiente=0
	total_pagado=0

	for p in pago:
		deuda += p.recargo
		deuda_pendiente = (p.deuda_pendiente + p.recargo)
		total_pagado  += p.pagos
	return render(request, "estadosDeCuenta.html",
			{
				'ajuste': ajuste,
				'pago': pago,
				'deuda': deuda,
				'deuda_pendiente': deuda_pendiente,
				'total_pagado': total_pagado,
				'usuariofull': request.user.get_full_name,
				'nombre': request.user.first_name
			})


@login_required(login_url='/login/')
def GenerarFactura(request):
	deuda=0
	deuda_pendiente=0
	total_A_pagar=0
	usuario= request.user.get_full_name()

	pago = Pago.objects.all().filter(propietario=usuario)

	for p in pago:
		deuda += p.recargo
		total_A_pagar += (p.deuda_pendiente + p.recargo)


	return render(request, )



class ReportePersonasPDF(View):

	def cabecera(self,request,pdf):
		usuario = request.user.get_full_name()
		propietario = Residente.objects.filter(nombre=usuario)

		#Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
		archivo_imagen = settings.MEDIA_ROOT+'Logo2.png'
		#Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 30, 700, 120, 90, preserveAspectRatio=True)
		pdf.setFont("Helvetica", 9)
		pdf.drawString(550, 770, u"%s" %time.strftime("%x"))

		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ['Estado de Cuenta'.upper()]
		#Creamos una lista de tuplas que van a contener a las personas
		# for p in propietario:
		# 	apartament = p.no_apartamento
		# 	edific = p.edificio


		detalles = [('%s, Edificio %s, Apartamento %s' %(usuario, p.edificio, p.no_apartamento)) for p in Residente.objects.filter(nombre=usuario)]
		# detalles = [('%s' %usuario), (', Edificio %s' %edific), (', Apartamento %s' %apartament)]

		#Establecemos el tamaño de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + [detalles], rowHeights=50, colWidths=[575])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
		[
				#La primera fila(encabezados) va a estar centrada
				('VALIGN',(0,0),(-1,-1),'MIDDLE'),
				('ALIGN',(0,0),(0,-1),'CENTER'),
				('FONTSIZE', (0, 0), (-1, -1), 12),
				('VALIGN',(0,0),(-1,-1),'MIDDLE'),
				('ALIGN',(0,0),(0,0),'CENTER'),
				('FONTSIZE', (0, 0), (-1, 0), 16),
				('TEXTCOLOR',(0,1),(-1,-1),colors.black),
				]
		))

		#Establecemos el tamaño de la hoja que ocupará la tabla
		detalle_orden.wrapOn(pdf, 1000, 800)
		#Definimos la coordenada donde se dibujará la tabla
		detalle_orden.drawOn(pdf, 15, 660)

	def tabla(self,request,pdf,y):
		usuario = request.user.get_full_name()
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ( 'FECHA', 'APTO', 'PAGO', 'CONCEPTO', 'PENDIENTE' , 'RECARGO', 'CONCEPTO REC.')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(p.fecha, p.no_edificio, 'RD$%s%s' %(p.pagos, '.00'), p.concepto, 'RD$%s%s' %(p.deuda_pendiente, '.00'), 'RD$%s%s' %(p.recargo, '.00'), p.concepto_deuda) for p in Pago.objects.filter(propietario__nombre=usuario)]
		#Establecemos el tamaño de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, rowHeights=15, colWidths=[
			12 * 5, 10 * 4, 15 * 5, 25 * 5, 15 * 5, 15 * 5, 25 * 5])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
		[
				#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(0,0),'CENTER'),
				#Los bordes de todas las celdas serán de color negro y con un grosor de 1
				('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
				('BOX', (0,0), (-1,-1), 0.75, colors.black),
				#El tamaño de las letras de cada una de las celdas será de 10
				('BACKGROUND', (0, 0), (8, 0), colors.lightblue),
				('ALIGN', (0, 0), (-5,-1), 'CENTER'),
				('ALIGN', (4, 0), (-2,-1), 'CENTER'),
				('FONTSIZE', (0, 0), (-1, -1), 7),
				('ALIGN',(0,0),(-1,0),'CENTER'),
				('VALIGN',(0,0),(-1,-1),'MIDDLE'),
				('FONTSIZE', (0, 0), (-1, 0), 9),
				]
		))
		#Establecemos el tamaño de la hoja que ocupará la tabla
		detalle_orden.wrapOn(pdf, 1000, 800)
		#Definimos la coordenada donde se dibujará la tabla
		detalle_orden.drawOn(pdf, 15, y)


	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer, pagesize=letter)
		#Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(request,pdf)
		y = 600
		self.tabla(request,pdf, y)
		#Con show page hacemos un corte de página para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response


# Libreria para PDF -- wkxhtm2pdf
