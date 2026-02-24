from django.db import models
from django.conf import settings
import datetime
from django.contrib.auth.models import User

class Tipo_muestra(models.Model):
    tipo_muestra=models.CharField(verbose_name="Tipo de muestra", max_length=90, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
   
    def __str__(self):    
        return(self.tipo_muestra) 

class Ensayo(models.Model):
    nombre_ensayo=models.CharField(verbose_name="Ensayo", max_length=90, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
   
    def __str__(self):    

        return(self.nombre_ensayo) 
    
class Metodo(models.Model):
    codigo_metodo=models.CharField(verbose_name="código", max_length=90, unique=True)
    nombre_metodo=models.CharField(verbose_name="Nombre", max_length=90, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
   
    def __str__(self):    

        return(self.codigo_metodo) 
        
class Etapa(models.Model):
    nombre_etapa=models.CharField(verbose_name="Etapa", max_length=90)
    ensayo=models.ForeignKey(to=Ensayo, on_delete=models.CASCADE, verbose_name="Ensayo", null=True, blank=False)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nombre_etapa', 'ensayo'], name='etapa'),
        ]
    def etapa(self):
        return "{} {}".format(self.nombre_etapa, self.ensayo)    
    def __str__(self):    
        return str(self.etapa())      

class EstadoProtocolo(models.Model):
    estado_protocolos=models.CharField(verbose_name="Estado Protocolos", max_length=90)
    estado_motivo=models.CharField(verbose_name="Motivo del estado", max_length=90, blank=True, null=False, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")
    def estado_protocolo(self):
        return "{} {}".format(self.estado_protocolos, self.estado_motivo)    
    def __str__(self):    
        return str(self.estado_protocolo())   
           
class Metodologia(models.Model):
    nombre_metodologia=models.CharField(verbose_name="Metodologia", max_length=90, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
    def __str__(self):
         return(self.nombre_metodologia) 
    
class Subparametro(models.Model):
    nombre_subparametro=models.CharField(max_length=90, verbose_name="Subparametro", blank=True, null=False, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
    def nombre_subparamtro_completo(self):
        return "{}".format(self.nombre_subparametro.__str__())       
    def __str__(self):    
        return str(self.nombre_subparamtro_completo())     
            
class Titulo_Parametro(models.Model):
    titulo_parametro=models.CharField(max_length=90, verbose_name="Titulo Párametro", blank=True, null=False, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
    def nombre_titulo_parametro(self):
        return "{}".format(self.titulo_parametro)    
    def __str__(self):    
        return str(self.nombre_titulo_parametro())

class Parametro(models.Model):
    nombre_titulo=models.ForeignKey(to=Titulo_Parametro, on_delete=models.CASCADE, verbose_name="Titulo Parametro", null=True, blank=False)
    nombre_parametro=models.OneToOneField(Subparametro, on_delete=models.CASCADE, verbose_name="Nombre Parametro", null=True, blank=True, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
    def nombre_Parametro(self):
        return "{} {}".format(self.nombre_titulo, self.nombre_parametro)    
    def __str__(self):    
        return str(self.nombre_Parametro())    

class Viabilidad(models.Model):
    nombre_viabilidad=models.CharField(verbose_name="Insumos del Proceso", max_length=90, null=True, blank=False, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
    def __str__(self):    
        return(self.nombre_viabilidad)
    
class Muestras_y_Placebos(models.Model):
    fecha_ingreso=models.DateField(verbose_name="Fecha de ingreso muestra", null=True, blank=False, help_text=u"AAAA/MM/DD")
    nombre_muestra=models.CharField(max_length=300, verbose_name="nombre de Muestra/Placebo/MP")
    tipo_muestra=models.ForeignKey(to=Tipo_muestra, on_delete=models.CASCADE, verbose_name="Tipo de muestra", null=True, blank=False)
    etapa=models.ForeignKey(to=Etapa, on_delete=models.CASCADE, verbose_name="Etapa", null=True, blank=False)
    codigo_muestra_interno=models.CharField(verbose_name="CIM / LIMS", max_length=90)
    codigo_muestra_producto=models.CharField(verbose_name="Código de Producto", max_length=90)
    lote_muestra=models.CharField(verbose_name="Lote", max_length=90)
    observaciones_muestras=models.TextField(max_length=300, verbose_name="Observaciones")
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion") 
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lote_muestra', 'etapa'], name='unique_intro'),
        ] 
    def nombre_muestras_y_placebos(self):
         return "{} {} {} {} {} {} {} {} {} {} {}".format(self.codigo_muestra_interno, self.nombre_muestra,(","), ("Código:"), self.codigo_muestra_producto,(","), ("Lote:"), self.lote_muestra,(","), ("Etapa:"), self.etapa )
    def __str__(self):    
        return str(self.nombre_muestras_y_placebos())      
class Cliente(models.Model):
    nombre_cliente=models.CharField(verbose_name="Cliente", max_length=90, null=True, blank=False, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
    def __str__(self):    
        return(self.nombre_cliente)

class Celda(models.Model):
    nombre_celda=models.CharField(verbose_name="Nombre de Celda", max_length=90, null=True, blank=False, unique=True)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")
    responsable = models.OneToOneField(User, on_delete=models.CASCADE)  
    def __str__(self):    
        return(self.nombre_celda)        

class Protocolos(models.Model):
     fecha_ingreso=models.DateField(verbose_name="Fecha de Registro", null=True, blank=False, help_text=u"AAAA/MM/DD")
     codigo=models.CharField(max_length=90, verbose_name="Código Protocolo", null=True, blank=False, unique=True)
     nombre=models.CharField(max_length=250, verbose_name="Título_del_Protocolo",  null=True, blank=False, unique=True)
     ensayo=models.ForeignKey(to=Ensayo, on_delete=models.CASCADE, verbose_name="Ensayo", null=True, blank=False)
     metodo=models.ForeignKey(to=Metodo, on_delete=models.CASCADE, verbose_name="Metodo de referencia", null=True, blank=False)
     celda=models.ForeignKey(to=Celda, on_delete=models.CASCADE, verbose_name="Celda", null=True, blank=False)
     muestras_y_Placebos=models.ManyToManyField(Muestras_y_Placebos, blank=False)
     metodologia=models.ForeignKey(Metodologia, on_delete=models.CASCADE, verbose_name="metodologia", null=True, blank=False,  max_length=90)
     parametro=models.ManyToManyField(to=Parametro, blank=False, related_name="parametro")
     Insumos_del_Proceso=models.ManyToManyField(to=Viabilidad)
     cliente=models.ForeignKey(to=Cliente, on_delete=models.CASCADE, verbose_name="Cliente", null=True, blank=False)
     estado_protocolo=models.ForeignKey(to=EstadoProtocolo, on_delete=models.CASCADE, verbose_name="Estado Protocolo", null=True, blank=False)
     class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
     condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
     observaciones=models.CharField(max_length=250, verbose_name="Observaciones",  null=True, blank=False)
     fecha_final=models.DateField(verbose_name="Fecha de Finalización", null=True, blank=True,default=datetime.datetime.now)
     fecha_de_entrega=models.DateField(verbose_name="Fecha de Entrega", null=True, blank=True, help_text=u"AAAA/MM/DD")
     entregado_a=models.CharField(max_length=250, verbose_name="Entregado a",  null=True, blank=True)
     def __str__(self):    
        return (self.codigo)
    

