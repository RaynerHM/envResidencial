from django.contrib import admin

# Register your models here.
from .models import Residente, Apartamento, Pago, Estado, Ajuste


class AdminResidentes(admin.ModelAdmin):
	list_display = ["nombre", 'edificio', 'no_apartamento', 'correo', 'telefono', 'cedula', 'clave']

	class Meta:
		model = Residente

admin.site.register(Residente, AdminResidentes)


class AdminApartamento(admin.ModelAdmin):
	list_display = ['no_edificio', 'no_apartamento', "propietario"]

	class Meta:
		model = Apartamento

admin.site.register(Apartamento, AdminApartamento)


class AdminPagos(admin.ModelAdmin):
	list_display = ['fecha', 'propietario', 'no_edificio', 'pagos', 'concepto', 'deuda_pendiente', 'recargo', 'concepto_deuda']
	class Meta:
		model = Pago

admin.site.register(Pago, AdminPagos)



class AdminAjustes(admin.ModelAdmin):
	list_display = ['fecha_Para_Facturar', 'monto_Manteniento', 'fecha_Limite_Pago', 'pago_Recargo']
	class Meta:
		model = Ajuste

admin.site.register(Ajuste, AdminAjustes)



class AdminEstado(admin.ModelAdmin):
	list_display = ['estado']
	class Meta:
		model = Estado

admin.site.register(Estado, AdminEstado)