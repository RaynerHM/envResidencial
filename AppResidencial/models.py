from django.db import models

# Create your models here.
from datetime import date
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser




class Residente(AbstractUser):
	telefono = models.CharField(max_length=10, blank=False, null=False)
	cedula = models.CharField(max_length=11, blank=False, null=False)
	no_apartamento = models.CharField(
		_("Apartamento"), max_length=5, blank=False, null=False)
	edificio = models.CharField(
		_("Edificio"), max_length=5, blank=False, null=False)
	avatar = models.ImageField(
		upload_to='avatares/', default='avatares/avatar.png')


	def __str__(self):
		return self.get_full_name()

class Apartamento(models.Model):
	no_edificio = models.CharField(
		_("Edificio"), max_length=15, blank=False, null=False)
	no_apartamento = models.CharField(
		_("Apartamento"), max_length=15, blank=False, null=False)
	propietario = models.ForeignKey(
		'Residente', on_delete=models.SET, blank=True, null=True)

	def __str__(self):
		apartament = self.no_edificio + ' - ' + self.no_apartamento
		return apartament


class Pago(models.Model):

	ESTADOS = (
		('Pendiente', 'Pendiente'),
		('Vigente', 'Vigente'),
		('Vencido', 'Vencido'),
		('Pagado', 'Pagado'),
	)
	propietario = models.ForeignKey(
		'Residente', on_delete=models.SET, blank=True, null=True)
	fecha = models.DateField(_("Fecha"), auto_now_add=True)
	# no_edificio = models.ForeignKey(
	# 	'Residente', on_delete=models.SET, blank=True, null=True, related_name='edificio')
	# no_edificio = models.ForeignKey(
	# 	'Apartamento', on_delete=models.SET, blank=True, null=False, default='0')
	pagos = models.DecimalField(
		max_digits=10, decimal_places=2, blank=False, null=False)
	concepto = models.CharField(max_length=70, blank=False, null=False)
	deuda_pendiente = models.DecimalField(
		max_digits=10, decimal_places=2, blank=False, null=False)
	recargo = models.DecimalField(
		max_digits=10, decimal_places=2, blank=False, null=False)
	concepto_deuda = models.CharField(
		max_length=70, blank=False, null=False, default="N/A")
	estado = models.CharField(
		max_length=20, blank=True, null=False, choices=ESTADOS)

	def __str__(self):
		return str(self.deuda_pendiente)
		# return self.recargo


class Ajuste(models.Model):

	fecha_Para_Facturar = models.DateField(
		_("Fecha Para Facturar"), editable=True, blank=False, null=False)
	monto_Manteniento = models.DecimalField(
		max_digits=10, decimal_places=2, blank=False, null=False)
	fecha_Limite_Pago = models.DateField(
		_("Fecha Limite De Pago"), editable=True, blank=False, null=False)
	pago_Recargo = models.DecimalField(
		max_digits=10, decimal_places=2, blank=False, null=False)

	# def __str__(self):
	# 	return self.fecha_Para_Facturar


class Estado(models.Model):
	ESTADOS = (
            ('Pendiente', 'Pendiente'),
            ('Vigente', 'Vigente'),
            ('Vencido', 'Vencido'),
            ('Listo', 'Listo'),
        )
	estado = models.CharField(max_length=20, blank=True, null=False, choices=ESTADOS)

	def __str__(self):
		return self.estado


class Sugerencia(models.Model):
	ESTADOS = (
		('Pendiente', 'Pendiente'),
		('Listo', 'Listo'),
	)
	propietario = models.ForeignKey(
		'Residente', on_delete=models.SET, blank=True, null=True)
	titulo = models.CharField(max_length=50, blank=False, null=False)
	sugerencia = models.TextField(blank=False, null=False)
	estado = models.CharField(max_length=15, blank=False, null=False, choices=ESTADOS)

	def __str__(self):
		return self.titulo


class Edificio(models.Model):
	bloque = models.IntegerField()
	apartamento = models.IntegerField()

	def __str__(self):
		return ('%s - %s' % (self.bloque, self.apartamento))
