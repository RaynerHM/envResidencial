from django.db import models
# Create your models here.
from datetime import date
from django.utils.translation import gettext as _

class Residente(models.Model):
	nombre = models.CharField(max_length=30, blank=False, null=False)
	correo = models.EmailField(max_length=50, blank=True, null=True)
	clave = models.CharField(max_length=15, blank=False, null=False)
	telefono = models.CharField(max_length=10, blank=False, null=False)
	cedula = models.CharField(max_length=11, blank=False, null=False)
	no_apartamento = models.CharField(max_length=5, blank=False, null=False)
	edificio = models.CharField(max_length=5, blank=False, null=False)
	def __str__(self):
		return self.nombre


class Apartamento(models.Model):
	no_edificio = models.CharField(max_length=15, blank=False, null=False)
	no_apartamento = models.CharField(max_length=15, blank=False, null=False)
	propietario = models.ForeignKey('Residente', on_delete=models.CASCADE, blank=False, null=True)
	
	def __str__(self):
		apartament = self.no_edificio +' - '+ self.no_apartamento
		return apartament


class Pago(models.Model):

	propietario = models.ForeignKey('Residente',on_delete=models.CASCADE, blank=False, null=False)
	fecha = models.DateField(_("Fecha"), auto_now_add=True)
	no_edificio = models.ForeignKey('Apartamento',on_delete=models.CASCADE, blank=False, null=False, default='0')
	pagos = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
	concepto = models.CharField(max_length=70, blank=False, null=False)
	deuda_pendiente = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
	recargo = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
	concepto_deuda = models.CharField(max_length=70, blank=False, null=False, default="N/A")
	
	def __str__(self):
		return self.fecha.strftime('%M')
		# return self.recargo


class Ajuste(models.Model):

	fecha_Para_Facturar = models.DateField(_("Fecha Para Facturar"), editable=True, blank=False, null=False)
	monto_Manteniento = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
	fecha_Limite_Pago = models.DateField(_("Fecha Limite De Pago"), editable=True, blank=False, null=False)
	pago_Recargo = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

	# def __str__(self):
	# 	return self.fecha_Para_Facturar


class Estado(models.Model):
	estado= models.CharField(max_length=20, blank=True, null=False)
	
	def __str__(self):
		return self.estado
