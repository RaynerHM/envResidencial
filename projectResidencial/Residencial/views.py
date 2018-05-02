from django.shortcuts import render

from .models import Residente, Apartamento, Pago

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from io import BytesIO
from reportlab.pdfgen import canvas
from datetime import *
from dateutil.relativedelta import *


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



@login_required
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
            {'nombre': v_nombre})
        else:
            return render(request, "registro_residente.html")
    return render(request, "registro_residente.html")
        


@login_required
def CambiarClave(request):
    v_clave_Vieja = request.POST.get("pass-last")
    v_clave_Nueva = request.POST.get("pass-new")

    if v_clave_Vieja != '' and v_clave_Nueva != '':
        try:
            clave = User.objects.get(username=v_clave_Vieja)        
            if clave == v_clave_Vieja:
                clave.set_password(v_clave_Nueva)
                clave.save()
                mensaje="Clave cambiada exitosamente"        
            else:
                mensaje="Fallo al cambiar la clave"
            return render(request, "password.html", {'mensaje': mensaje})
            
        except User.DoesNotExist:
            clave = None
    return render(request, "password.html")
    


@login_required
def Sesion(request):
    return render(request, "sesion.html")
    


@login_required
def EstadosCuenta(request):
    pago = Pago.objects.all()
    deuda=0
    deuda_pendiente=0
    total_pagado=0

    for d in pago:
        deuda += d.recargo
        deuda_pendiente = (d.deuda_pendiente + d.recargo)
        total_pagado  += d.pagos
    return render(request, "estadosDeCuenta.html", 
        {'pago': pago,
        'deuda': deuda,
        'deuda_pendiente': deuda_pendiente,
        'total_pagado': total_pagado,       
        'usuariofull': request.user.get_full_name,
        'usuario': request.user })


    
@login_required
def hello_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prueba.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.drawString(100, 100, "p.propietario")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
