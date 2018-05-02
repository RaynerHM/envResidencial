from django import forms
from .models import Residente, Apartamento, Pago


#class FormResidente(forms.ModelForm):
#    class Meta:
#        model = Residente
#        fields = ["propietario", 'correo', 'telefono', 'cedula', 'clave']
class RegResidente(forms.Form):
    propietario = forms.CharField(max_length=30)
    correo = forms.EmailField(max_length=50)
    telefono = forms.CharField(max_length=15)
    cedula = forms.CharField(max_length=10)
    clave = forms.CharField(max_length=10)
