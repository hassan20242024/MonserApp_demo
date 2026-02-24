from django import forms
from django.contrib import admin
from django.forms.widgets import NumberInput
from django.contrib.admin.widgets import AutocompleteSelect
from django_select2 import forms as s2forms
from .models import Protocolos, Parametro, Metodologia, EstadoProtocolo,Ensayo,Viabilidad, Subparametro,Titulo_Parametro, Muestras_y_Placebos, Cliente, Celda, Metodo, Tipo_muestra, Etapa
from Aplicaciones.Secuencias.models import Sistema
from Aplicaciones.Protocolo_Muestras.models import ViabilidadProceso


class ProtocolosForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'placeholder': 'Título del Protocolo'}))
    fecha_ingreso=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    fecha_de_entrega=forms.DateField( required=False, widget=NumberInput(attrs={'type': 'date'}))
    Insumos_del_Proceso = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,queryset=Viabilidad.objects.all()
        )
    parametro = forms.ModelMultipleChoiceField(
        queryset=Parametro.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'id_parametro'})
    )
    muestras_y_Placebos = forms.ModelMultipleChoiceField(
        queryset=Muestras_y_Placebos.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'id_muestras_y_Placebos'})
    )
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':6}))

    class Meta:
        model=Protocolos
        fields = '__all__'
        exclude=["condicion"]

class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'
        exclude = ['condicion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_titulo'].required = True
        self.fields['nombre_parametro'].required = True

class SubparametroForm(forms.ModelForm):
    class Meta:
        model=Subparametro
        fields = '__all__'
        exclude=["condicion"] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_subparametro'].required = True

class Titulo_ParametroForm(forms.ModelForm):
    class Meta:
        model=Titulo_Parametro
        exclude=["condicion"]   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo_parametro'].required = True

class MetodologiaForm(forms.ModelForm):
    class Meta:
        model=Metodologia
        exclude=["condicion"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_metodologia'].required = True

class EstadoProtocoloForm(forms.ModelForm):
    class Meta:
        model=EstadoProtocolo
        exclude=["condicion"]  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado_protocolos'].required = True
        self.fields['estado_motivo'].required = True

class crear_ensayoForm(forms.ModelForm):
    class Meta:
        model=Ensayo
        exclude=["condicion"] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_ensayo'].required = True

class ViabilidadForm(forms.ModelForm):
    class Meta:
        model=Viabilidad
        exclude=["condicion"] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_viabilidad'].required = True

class ingresar_muestrasForm(forms.ModelForm):
    fecha_ingreso=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    observaciones_muestras = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    
    class Meta:
        fields = '__all__'
        model=Muestras_y_Placebos
        exclude=["condicion"]                     

class clienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        exclude=["condicion"] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_cliente'].required = True

class sistemaForm(forms.ModelForm):
    class Meta:
        model=Sistema
        fields = ['nombre', 'condicion'] 

class CeldaForm(forms.ModelForm):
    class Meta:
        model=Celda
        exclude=["condicion"] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_celda'].required = True
        self.fields['responsable'].required = True

class MetodoForm(forms.ModelForm):
    class Meta:
        model = Metodo
        exclude = ["condicion"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que los campos sean obligatorios
        self.fields['codigo_metodo'].required = True
        self.fields['nombre_metodo'].required = True

        # Desactivar autocomplete
        self.fields['codigo_metodo'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['nombre_metodo'].widget.attrs.update({'autocomplete': 'off'})
        
class tipo_muestrasForm(forms.ModelForm):
    class Meta:
        model=Tipo_muestra
        exclude=["condicion"]  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_muestra'].required = True

class EtapaForm(forms.ModelForm):
    class Meta:
        model=Etapa
        exclude=["condicion"] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_etapa'].required = True
        self.fields['ensayo'].required = True

class viavilidad_procesoForm(forms.ModelForm):
    class Meta:
        model=ViabilidadProceso
        exclude=["condicion"]                                     



                 




         


  
        

   
        

   