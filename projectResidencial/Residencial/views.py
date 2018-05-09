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


		# if v_clave_Vieja != '' and v_clave_Nueva != '':
		#     try:
		#         clave = User.objects.get(username=request.user)
		#         if clave == v_clave_Vieja:
		#             clave.set_password(v_clave_Nueva)
		#             clave.save()
		#             mensaje="Clave cambiada exitosamente"        
		#         else:
		#             mensaje="Fallo al cambiar la clave"
		#         return render(request, "password.html", {'mensaje': mensaje})
				
		#     except User.DoesNotExist:
		#         clave = None
	return render(request, "password.html")
	

@login_required(login_url='/login/')
def Sesion(request):
	return render(request, "sesion.html")
	

@login_required(login_url='/login/')
def EstadosCuenta(request):
	usuario= request.user.get_full_name()
	
	ajuste = Ajuste.objects.all()
	# for a in ajustes:
	#     fecha_Para_Facturar = a.fecha_Para_Facturar
	#     monto_Manteniento = a.monto_Manteniento
	#     fecha_Limite_Pago = a.fecha_Limite_Pago
	#     pago_Recargo = a.pago_Recargo


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
				'usuario': request.user 
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

	
# @login_required(login_url='/login/')
# def hello_pdf(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="prueba.pdf"'

#     buffer = BytesIO()

#     # Create the PDF object, using the BytesIO object as its "file."
#     p = canvas.Canvas(buffer)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.

#     p.drawString(100, 100, "p.propietario")

#     # Close the PDF object cleanly.
#     p.showPage()
#     p.save()

#     # Get the value of the BytesIO buffer and write it to the response.
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#     return response


@login_required(login_url='/login/')
class GenerarPDF(View):
	
	def get(request, *args, **kwargs):
		
		usuario= request.user.get_full_name()
		pago = Pago.objects.all().filter(propietario__nombre=usuario)
		
		deuda=0
		deuda_pendiente=0
		total_pagado=0

		for p in pago:
			deuda += p.recargo
			deuda_pendiente = (p.deuda_pendiente + p.recargo)
			total_pagado  += p.pagos
	   

		pdf = render_pdf("reporte.html", 
			{'pago': pago,
			'deuda': deuda,
			'deuda_pendiente': deuda_pendiente,
			'total_pagado': total_pagado,       
			'usuariofull': request.user.get_full_name,
			'usuario': request.user })
		return HttpResponse(pdf, content_type="application/pdf")



class ReportePersonasPDF(View):
	
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
		archivo_imagen = settings.MEDIA_ROOT+'/logo2.png'
		#Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 30, 710, 120, 90, preserveAspectRatio=True)
		#Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
		#Dibujamos una cadena en la ubicación X,Y especificada
		# pdf.setFont("Helvetica", 16)
		# pdf.drawString(230, 755, u"Residencial Brisa Fresca")
		pdf.setFont("Helvetica", 16)
		pdf.drawString(260, 735, u"Estado de Cuenta")
		pdf.setFont("Helvetica", 9)
		pdf.drawString(550, 770, u"%s" %time.strftime("%x"))


	def tabla(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Propietario', 'Fecha', '# Edif.', 'Pagos', 'Concepto', 'Pendiente' , 'Recargo', 'Concepto Deuda')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(p.propietario, p.fecha, p.no_edificio, 'RD$%s' %p.pagos, p.concepto, 'RD$%s' %p.deuda_pendiente, 'RD$%s' %p.recargo, p.concepto_deuda) for p in Pago.objects.all()]
		#Establecemos el tamaño de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, rowHeights=15, colWidths=[
			25 * 5, 12 * 5, 10 * 4, 10 * 5, 20 * 5, 10 * 5, 10 * 5, 20 * 5])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
		[
				#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(0,0),'CENTER'),
				#Los bordes de todas las celdas serán de color negro y con un grosor de 1
				('GRID', (0, 0), (-1, -1), 1, colors.black),
				#El tamaño de las letras de cada una de las celdas será de 10
				('FONTSIZE', (0, 0), (-1, -1), 12),
				('BACKGROUND', (0, 0), (8, 0), colors.lavender),
				('FONTSIZE', (0, 0), (-1, -1), 8),
				]
		))
		#Establecemos el tamaño de la hoja que ocupará la tabla
		detalle_orden.wrapOn(pdf, 1000, 800)
		#Definimos la coordenada donde se dibujará la tabla
		detalle_orden.drawOn(pdf, 20, y)


	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer, pagesize=letter)
		#Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf)
		y = 600
		self.tabla(pdf, y)
		#Con show page hacemos un corte de página para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response



		doc = SimpleDocTemplate("simple_table_grid.pdf", pagesize=letter)
		# container for the 'Flowable' objects
		elements = []
		
		data= [['00', '01', '02', '03', '04'],
			['10', '11', '12', '13', '14'],
			['20', '21', '22', '23', '24'],
			['30', '31', '32', '33', '34']]
		t=Table(data,5*[0.4*inch], 4*[0.4*inch])
		t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
							('TEXTCOLOR',(1,1),(-2,-2),colors.red),
							('VALIGN',(0,0),(0,-1),'TOP'),
							('TEXTCOLOR',(0,0),(0,-1),colors.blue),
							('ALIGN',(0,-1),(-1,-1),'CENTER'),
							('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
							('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
							('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
							('BOX', (0,0), (-1,-1), 0.25, colors.black),
							]))
		
		elements.append(t)
		# write the document to disk
		doc.build(elements)


# Libreria para PDF -- wkxhtm2pdf
