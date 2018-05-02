from django.contrib import admin

# Register your models here.
from .models import Residente, Apartamento, Pago


class AdminResidentes(admin.ModelAdmin):
    	# list_display = ["nombre", "departamento"]
	list_display = ["nombre", 'no_apartamento', 'edificio', 'correo', 'telefono', 'cedula', 'clave']

	class Meta:
		model = Residente

admin.site.register(Residente, AdminResidentes)


class AdminApartamento(admin.ModelAdmin):
    	# list_display = ["nombre", "departamento"]
	list_display = ['no_edificio', 'no_apartamento', "propietario"]

	class Meta:
		model = Apartamento

admin.site.register(Apartamento, AdminApartamento)


class AdminPagos(admin.ModelAdmin):
    	# list_display = ["nombre", "departamento"]
	# list_display = ["propietario", 'no_edificio', 'pagos']
	list_display = ['fecha', 'propietario', 'no_edificio', 'pagos', 'concepto', 'deuda_pendiente', 'recargo', 'concepto_deuda']
	class Meta:
		model = Pago

admin.site.register(Pago, AdminPagos)


