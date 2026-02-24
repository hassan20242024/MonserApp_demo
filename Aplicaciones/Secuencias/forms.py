from django import forms
from django.contrib import admin
from django.forms.widgets import NumberInput
from django.contrib.admin.widgets import AutocompleteSelect
from django_select2 import forms as s2forms
from .models import Protocolos,Sistema,Parametro,Lavado_buzo
from django.core.exceptions import ValidationError
from django.core import validators

from .models import Secuencias

class secuenciasForm(forms.ModelForm):
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), required=True)
    class Meta:
        model=Secuencias
        fields = '__all__'

class buzosForm(forms.ModelForm):
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':8}), required=True)
    class Meta:
        model= Lavado_buzo
        fields = '__all__'
        exclude = ["condicion"]


class LavadoBuzoForm(forms.ModelForm):
    class Meta:
        model = Lavado_buzo
        fields = [
            'sistema',
            'fecha_lavado_buzo',
            'fecha_lavado_celda',
            'fecha_test_diagnostico',
            'fecha_mantenimiento',
            'fecha_calificacion',
            'observaciones'
        ]
        widgets = {
            'fecha_lavado_buzo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_lavado_celda': forms.DateInput(attrs={'type': 'date'}),
            'fecha_test_diagnostico': forms.DateInput(attrs={'type': 'date'}),
            'fecha_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_calificacion': forms.DateInput(attrs={'type': 'date'}),
        }



