from django.shortcuts import render

# Create your views here.
from AppResidencial.models import *
from django.conf import settings

from django.contrib import auth
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
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

import time
import datetime
from dateutil.relativedelta import *

from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives

from django.core import serializers
import json


def login(request):
	mensaje = ''
	if request.method == 'POST':
		v_usuario = request.POST.get('username')
		v_clave = request.POST.get('password')

		usuario = authenticate(username=v_usuario, password=v_clave)

		if usuario is not None:
			if usuario.is_active == False:
				print('El Usuario no esta activo.')
				mensaje = """
				Su cuanta de usuario esta desactivada.
				Por favor, pongase en contacto con el administrador de este
				Website."""
				print(mensaje)
			else:
				auth.login(request, usuario)
				return redirect(estados_cuenta)
		else:
			mensaje = 'Usuario o clave incorrecto'
			print(mensaje)
	return render(request, 'login.html', {'mensaje': mensaje})


@login_required()
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login")


def registrar_usuario(request):
	mensaje = ''
	if request.method == 'POST':
		v_nombre = request.POST.get('nombre')
		v_apellido = request.POST.get('apellido')
		v_correo = request.POST.get("correo")
		v_no_apartamento = request.POST.get("apartamento")
		v_edificio = request.POST.get("edificio")
		v_telefono = request.POST.get("telefono")
		v_cedula = request.POST.get("cedula")
		v_clave = request.POST.get("clave")

		v_telefono = v_telefono.split('-')
		# v_telefono = (v_telefono[0] + v_telefono[1] + v_telefono[2])
		v_telefono = v_telefono
		v_cedula = v_cedula.split('-')
		# v_cedula = (v_cedula[0] + v_cedula[1] + v_cedula[2])
		v_cedula = v_cedula

		if (v_nombre != '' and v_apellido != '' and v_correo != ''
			and v_telefono != '' and v_cedula != '' and v_clave != ''):

			if Residente.objects.filter(username=v_correo).count():
				mensaje = """El correo '%s' ya esta registrado.
					Por favor valide que los datos sean correctos.""" %v_correo
			else:
				usuario = Residente.objects.create_user(
					username=v_correo,
					password=v_clave,
					first_name=v_nombre,
					last_name=v_apellido,
					email=v_correo,
					no_apartamento=v_no_apartamento,
					edificio=v_edificio,
					telefono=v_telefono,
					cedula=v_cedula,
				)
				usuario.is_active = True
				usuario.is_staff = False
				usuario.save()

				# Crear registro del Residente
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

				# Enviar correo con el usuario creado
				try:
					url = 'localhost:8000/'

					html_content = ("""
						<style>
							body {
								background-color: #fff;
							}
							div {
								text-align: center;
							}
							.padding {
								padding-top: 20px;
							}
							.felicidad {
								color: #00c853;
								font-size: 46px
							}
							h3 {
								font-size: 20px
							}
							.color {
								color: blue;
								font-size: 24px;
								padding-bottom:0px;
							}
							.usuario {
								margin-bottom: 0px;
								padding-bottom: 0px;
								font-size: 20px
							}
							a {
								font-size: 16px
							}
						</style>

						<div class="center-align padding">
							<div class="center-align padding">
								<div class="felicidad">¡Felicidades, %s!</div>
								<h3>Su cuenta ha sido creada exitosamente.</h3>
							</div>
							<div class="padding usuario">
							<h3> Su usuario es:</h3>
							<div class="color"> %s</div>
							</div>
							<div class="padding">
								<a href="%s" class="btn">Acceder a su cuenta</a>
							</div>
						</div>
						""" % (v_nombre, v_correo, url))

					subject, from_email, to = (
						'Cuenta Residencial Brisa Fresca',
						settings.EMAIL_HOST_USER, v_correo
					)
					text_content = (
						'Credenciales de su cuenta Residencial Brisa Fresca.'
					)
					msg = EmailMultiAlternatives(
						subject, text_content, from_email, [to]
					)
					msg.attach_alternative(html_content, "text/html")
					msg.send()
				except BadHeaderError:
					return HttpResponse('No se pudo enviar el correo.')

				datos = {
					'nombre': v_nombre,
					'correo': v_correo
				}

				return render(request, "felicidades.html", datos)
		else:
			return render(request, "registro_residente.html")
	return render(request, "registro_residente.html", {'mensaje': mensaje})

# ------------ Pendiente por terminar ------------
@login_required()
#@permission_required('Residencial.add_pago', raise_exception=True)
def cambiar_clave(request):
	return render(request, "password.html")


@login_required()
def registrar_pagos(request):

	deuda = 0
	ajuste = Ajuste.objects.all()[:1]

	if request.method == 'POST':
		v_apartamento = request.POST.get('apartamento')
		v_bloque = request.POST.get('bloque')
		v_montoPagar = request.POST.get('montoPagar')
		v_concepto = request.POST.get('concepto')
		monto_Manteniento = int(ajuste[0].monto_Manteniento)

		if int(v_montoPagar) < monto_Manteniento:
			deuda = int(v_montoPagar) - monto_Manteniento
		else:
			deuda = 0

		"""
		pago= Pago.objects.create(
			propietario,
			fecha,
			no_edificio,
			pagos = v_montoPagar,
			concepto = v_concepto,
			deuda_pendiente = deuda,
			recargo,
			concepto_deuda,
			estado
		)
		"""

		print(deuda)
		print('\n\nBloque:__________ %s\nApartamento:_____ %s\nMonto:___________ %s\nConcepto:________ %s\n' %
			  (v_bloque, v_apartamento, v_montoPagar, v_concepto))

	lista_personas = []
	v_nombre = request.POST.get('persona', '')
	print(v_nombre)
	# v_nombre = ""
	if v_nombre != "":
		residente = Residente.objects.filter(nombre__contains=v_nombre)
	else:
		residente = Residente.objects.all().order_by('edificio')

	for r in residente:
		p_dic = {
			'nombre': '',
			'apartamento': '',
			'pago': [],
		}
		p_dic['nombre'] = r.username
		p_dic['apartamento'] = r.edificio + '-' + r.no_apartamento

		pago = Pago.objects.all().filter(propietario__username=r.username)
		for p in pago:
			p_dic['pago'].append(p)

		lista_personas.append(p_dic)

	return render(request, "registrar_Pagos.html", {
			'pago': lista_personas,
			'res': residente
		})


# @login_required(login_url='/login/')
def EnviarCorreo(request):
	try:
		usuario = request.user.first_name
		correo = request.user.email
		url = 'http://10.1.100.200:8000/login'

		html_content = ("""
			<style>
				body {
					background-color: #fff;
				}
				div {
					text-align: center;
				}
				.padding {
					padding-top: 20px;
				}
				.felicidad {
					color: #00c853; font-size: 46px
				}
				h3 {
					font-size: 20px
				}
				.color {
					color:blue; font-size: 24px;
					padding-bottom:0px;
				}
				.usuario {
					margin-bottom:0px;
					padding-bottom:0px;
					font-size: 20px;
				}
				a {
					font-size: 16px
				}
			</style>

			<div class="center-align padding">
				<div class="center-align ">
					<div class="felicidad">¡Felicidades, %s!</div>
					<h3>Su cuenta ha sido creada exitosamente.</h3>
				</div>
				<div class="padding usuario">
				<h3> Su usuario es:</h3>
				<br>
				<div class="color"> %s</div>
				</div>
				<div class="padding">
					<a href="%s" class="btn">Acceder a su cuenta</a>
				</div>
			</div>
			""" % (usuario, correo, url))

		subject, from_email, to = (
			'Cuenta Residencial Brisa Fresca', 'raynel95@gmail.com', correo
		)
		text_content = 'Credenciales de su cuenta Residencial Brisa Fresca.'
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
	except BadHeaderError:
		return HttpResponse('No se pudo enviar el correo.')
	# return HttpResponseRedirect('/')
	return render(request, 'felicidades.html')

	# asunto = request.POST.get('subject', '')
	# mensaje = request.POST.get('message', '')
	# desde = 'raynel95@gmail.com'
	# if asunto and mensaje and from_email:
	#     try:
	#         send_mail(asunto, mensaje, desde, 'Enviar a:')
	#     except BadHeaderError:
	#         return HttpResponse('No se pudo enviar el correo.')
	#     return HttpResponseRedirect('/')
	# else:
	#     # In reality we'd use a form class
	#     # to get proper validation errors.
	#     return HttpResponse('Asegúrese de que todos los campos estén ingresados ​​y sean válidos.')


def guardar_ajax(request):
	print(request.POST)
	if request.method == 'POST':
		id_deuda = request.POST.get('deudas')
		# print(id_deuda.split(','))
		# id_deuda=id_deuda.split(',')
		# print('Tipo',type(id_deuda))
		# print(id_deuda)
		# pago = Pago.objects.filter(id=id_deuda.split(','))
		# id_deuda=[2,3,5]
		# pago = [Pago.objects.filter(id=asd for asd in id_deuda)]
		# print(str(pago[0].deuda_pendiente))
		# print(str(pago[0].estado))
		# print(str(pago[1].deuda_pendiente))
		# print(str(pago[1].estado))
		# print(str(pago[2].deuda_pendiente))
		# print(str(pago[2].estado))
		# print(str(pago[3].deuda_pendiente))
		# print(str(pago[3].estado))
		#pago.deuda_pendiente
		mensaje = '¡El pago se ha generado satisfactoriamente!'

		return HttpResponse(
			json.dumps({
				'mensaje': mensaje,
			}),
			content_type="application/json"
		)


def buscar_deuda_ajax(request):
	if request.method == 'POST':
		bloq = request.POST.get('bloq')
		apto = request.POST.get('apto')

		ajuste = Ajuste.objects.all()
		ajuste = [ajuste_serializer(ajuste) for ajuste in ajuste]

		residente = Residente.objects.filter(
			no_apartamento=apto, edificio=bloq
		)
		id_residente = residente[0].id
		# residente = [residente_serializer(residente)
		# for residente in residente]

		deuda = Pago.objects.filter(
			propietario=id_residente, deuda_pendiente__gte=1
		)
		# deuda = [deuda_serializer(deuda) for deuda in deuda]

		print('\n\n**************' )
		print(residente)
		print(type(residente))
		print('**************' )
		for residente in residente:
			print(residente )
		print('**************\n\n' )

		datos_residente = {
			# 'nombre': residente.get_full_name(),
			'nombre': str(residente.last_name),
			'correo': residente.email,
			'telefono': residente.telefono,
			'cedula': residente.cedula,
			'no_apartamento': residente.no_apartamento
		}

		# deuda_residente = {
		# 	'id': str(deuda.id),
		# 	'deuda_pendiente': str(deuda.deuda_pendiente),
		# 	'recargo': str(deuda.recargo),
		# 	'concepto_deuda': str(deuda.concepto_deuda)
		# }
		return HttpResponse(
			json.dumps({
				'residente': residente,
				'ajuste': ajuste,
				# 'deuda': deuda,
			}),
			content_type="application/json"
		)


def residente_serializer(residente):
	return {
		'nombre': residente.get_full_name(),
		'correo': residente.email,
		'telefono': residente.telefono,
		'cedula': residente.cedula,
		'no_apartamento': residente.no_apartamento
	}


def deuda_serializer(deuda):
	return {
		'id': str(deuda.id),
		'deuda_pendiente': str(deuda.deuda_pendiente),
		'recargo': str(deuda.recargo),
		'concepto_deuda': str(deuda.concepto_deuda)
	}


def ajuste_serializer(ajuste):
	return {
		'fecha_Limite_Pago': str(ajuste.fecha_Limite_Pago),
		'pago_Recargo': str(ajuste.pago_Recargo)
	}


@login_required()
def estados_cuenta(request):
    	id_usuario = request.user.id
	ajuste = Ajuste.objects.all()

	pago = Pago.objects.all().filter(propietario=request.user.id)
	deuda = 0
	deuda_pendiente = 0
	total_pagado = 0
	for p in pago:
		deuda += p.recargo
		deuda_pendiente = (p.deuda_pendiente + p.recargo)
		total_pagado += p.pagos

	datos = {
		'ajuste': ajuste,
		'pago': pago,
		'deuda': deuda,
		'deuda_pendiente': deuda_pendiente,
		'total_pagado': total_pagado,
	}
	return render(request, "estadosDeCuenta.html", datos)


@login_required()
def GenerarFactura(request):
	deuda = 0
	total_A_pagar = 0
	usuario = request.user.get_full_name()

	pago = Pago.objects.all().filter(propietario=usuario)

	for p in pago:
		deuda += p.recargo
		total_A_pagar += (p.deuda_pendiente + p.recargo)

	return render(request, )


class reporte_estado_de_cuenta_personal(View):

	def cabecera(self, request, fecha, pdf):
		usuario = request.user.get_full_name()

		#Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
		archivo_imagen = settings.MEDIA_ROOT + 'Logo.png'

		#Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 30, 700, 120, 90,
			preserveAspectRatio=True
		)
		pdf.setFont("Helvetica", 9)
		# pdf.drawString(550, 770, u"%s" %time.strftime("%x"))
		pdf.drawString(500, 760, u"Fecha:  %s/%s/%s"
			%(fecha.day, fecha.month, fecha.year)
		)
		pdf.drawString(500, 750, u"Hora:           %s:%s"
			%(fecha.hour, fecha.minute)
		)

		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ['Estado de Cuenta'.upper()]

		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [
			('%s, Edificio %s, Apartamento %s'
			%(usuario, p.edificio,
			p.no_apartamento)) for p in
			Residente.objects.filter(id=request.user.id)
		]

		#Establecemos el tamaño de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + [detalles],
			rowHeights=50, colWidths=[575]
		)

		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(
			TableStyle(
				[
					#La primera fila(encabezados) va a estar centrada
					('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
					('ALIGN', (0, 0), (0, -1), 'CENTER'),
					('FONTSIZE', (0, 0), (-1, -1), 12),
					('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
					('ALIGN', (0, 0), (0, 0), 'CENTER'),
					('FONTSIZE', (0, 0), (-1, 0), 16),
					('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
				]
			)
		)

		#Establecemos el tamaño de la hoja que ocupará la tabla
		detalle_orden.wrapOn(pdf, 1000, 800)
		#Definimos la coordenada donde se dibujará la tabla
		detalle_orden.drawOn(pdf, 15, 660)

	def tabla(self, request, pago, pdf, y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('FECHA', 'PAGO', 'CONCEPTO', 'PENDIENTE',
					   'RECARGO', 'CONCEPTO RECARGO')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(p.fecha, 'RD$%s%s' %(p.pagos, '.00'),
			p.concepto, 'RD$%s%s' %(p.deuda_pendiente, '.00'), 'RD$%s%s'
			%(p.recargo, '.00'), p.concepto_deuda) for p in pago
		]

		#Establecemos el tamaño de cada una de las columnas de la tabla
		detalle_orden = Table(
			[encabezados] + detalles, rowHeights=15, colWidths=
			[
				12 * 5,
				15 * 5,
				30 * 5,
				15 * 5,
				15 * 5,
				30 * 5
			]
		)
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
				#La primera fila(encabezados) va a estar centrada
				('ALIGN', (0, 0), (0, 0), 'CENTER'),
				#Los bordes de todas las celdas serán de color negro y con un grosor de 1
				('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
				('BOX', (0, 0), (-1, -1), 0.75, colors.black),
				#El tamaño de las letras de cada una de las celdas será de 10
				('BACKGROUND', (0, 0), (8, 0), colors.lightblue),
				('ALIGN', (0, 0), (-5, -1), 'CENTER'),
				('ALIGN', (4, 0), (-2, -1), 'CENTER'),
				('FONTSIZE', (0, 0), (-1, -1), 7),
				('ALIGN', (0, 0), (-1, 0), 'CENTER'),
				('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
				('FONTSIZE', (0, 0), (-1, 0), 9),
			]
		))
		#Establecemos el tamaño de la hoja que ocupará la tabla
		detalle_orden.wrapOn(pdf, 1000, 800)
		#Definimos la coordenada donde se dibujará la tabla
		detalle_orden.drawOn(pdf, 15, y)

	def totales(self, request, pago, pdf, y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ['TOTALES']
		#Creamos una lista de tuplas que van a contener a las personas
		deuda = 0
		deuda_pendiente = 0
		total_pagado = 0

		for p in pago:
			deuda += p.recargo
			deuda_pendiente = (p.deuda_pendiente + p.recargo)
			total_pagado += p.pagos

		detalles = [
			['Total Deuda                                   RD$%s.00' %deuda],
			['Total Deuda Por Recargo             RD$%s.00' %deuda_pendiente],
			['Total Pagado                                 RD$%s.00'
			%total_pagado]
		]
		#Establecemos el tamaño de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles,
							  rowHeights=15, colWidths=[43 * 5])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(
			TableStyle(
				[
					('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
					('BACKGROUND', (0, 0), (8, 0), colors.lightblue),
					('INNERGRID', (0, 0), (0, 0), 0.25, colors.black),
					('ALIGN', (0, 0), (-1, -1), 'LEFT'),
					('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
					('ALIGN', (0, 0), (0, 0), 'CENTER'),
					('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
				]
			)
		)
		#Establecemos el tamaño de la hoja que ocupará la tabla
		detalle_orden.wrapOn(pdf, 1000, 800)
		#Definimos la coordenada donde se dibujará la tabla
		detalle_orden.drawOn(pdf, 380, 50)

	def get(self, request, *args, **kwargs):
		pago = Pago.objects.filter(id=request.user.id)
		fecha = datetime.datetime.now()
		fechaAct = "%s-%s-%s" % (fecha.day, fecha.month, fecha.year)
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = (
			'filename="Estado de Cuenta-' + fechaAct+'.pdf"'
		)
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer, pagesize=letter)
		#Titulo del PDF
		pdf.setTitle('Estado de Cuenta-'+fechaAct+'.pdf')
		#Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(request, fecha, pdf)
		y = 600
		self.tabla(request, pago, pdf, y)
		self.totales(request, pago, pdf, y)
		#Con show page hacemos un corte de página para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response


def sugerencias_ajax(request):
	if request.method == 'POST':
		user_id = int(request.POST.get('user_id'))
		titulo = request.POST.get('titulo')
		sugerencia = request.POST.get('sugerencia')
		estado = 'Pendiente'

		try:
			if user_id and titulo and sugerencia and estado:
				sugerencias = Sugerencia.objects.create(
					propietario_id = user_id,
					titulo = titulo,
					sugerencia = sugerencia,
					estado = estado
				)

				mensaje = (
					"""
					Su sugerencia ha sido enviada.
					¡Muchas gracias, la tomaremos en cuenta!
					"""
				)
				print('Datos Guardados\n\n')
		except Exception as ex:
			mensaje =("""
			La sugerencia no pudo ser enviada. Favor contacte con la Administración. \n%s
			""" %ex)
			print('\nERROR: %s\n\n' %ex)


		return HttpResponse(
			json.dumps({
				'mensaje': mensaje,
			}),
			content_type="application/json"
		)


def cambiar_clave_ajax(request):
	clave = Residente.objects.get(id=request.user.id)
	print(clave)
	print(request.user)
	mensaje = ''
	estado = 0

	cont = {
		'estado': 0,
		'mensaje': '',
	}
	if request.method == 'POST':
		v_clave_Nueva1 = request.POST.get("pass-new")
		print(v_clave_Nueva1)

		clave = Residente.objects.get(id=request.user.id)

		if v_clave_Nueva1:
			clave.set_password(v_clave_Nueva1)
			clave.save()

			cont['mensaje'] = "Clave cambiada exitosamente"
			cont['estado'] = 1

		else:
			cont['mensaje'] = "Fallo al cambiar la clave"
			cont['estado'] = 0

	return HttpResponse(
		json.dumps(cont),
		content_type="application/json"
	)


def cargar_nombres_ajax(request):
	if request.method == 'POST':
		datos = {	}

		nombres = Residente.objects.all()
		print(nombres)

		for	nom in nombres:
			avatar = '%s%s' %(settings.MEDIA_URL, nom.avatar)
			nombre = nom.get_full_name()
			datos[nombre] = avatar

		print(datos)

	return HttpResponse(
		json.dumps(datos),
		content_type="application/json"
	)


def configurar_usuarios(request):
	usuarios = Residente.objects.all()
	contenido={
		'usuarios': usuarios,
		'MEDIA_URL': settings.MEDIA_URL
	}
	print(contenido)
	return render(request, 'usuarios.html', contenido)
