
from django import forms
from django.forms.widgets import NumberInput
from .models import Proceso, ViabilidadProceso

class ProcesoForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'placeholder': 'Título del Protocolo'}))
    fecha_ingreso=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    fecha_de_entrega=forms.DateField( required=False, widget=NumberInput(attrs={'type': 'date'}))
    Insumos_del_Proceso = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,queryset=ViabilidadProceso.objects.all())
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':6}))
    class Meta:
        model=Proceso
        fields = '__all__'
        exclude=["condicion"]
        
