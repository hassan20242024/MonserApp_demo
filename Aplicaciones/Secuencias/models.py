from django.db import models
from django.conf import settings
from Aplicaciones.Protocolo_Metodos.models import Protocolos, Parametro, Ensayo, Muestras_y_Placebos, Metodo
from Aplicaciones.Protocolo_Muestras.models import Proceso
from Aplicaciones.perfiles.models import Perfil
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
import datetime
from django.utils import timezone

class Sistema(models.Model):
    nombre=models.CharField(max_length=250, verbose_name="Sistema",  null=True, blank=False)
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion")  
    
    def __str__(self):    

        return (self.nombre)

class usuario_invalidar(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.usuario.username   
class usuario_validar(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.usuario.username
           
class usuario_impresion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.usuario.username
    
class usuario_reporte(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.usuario.username

class usuario_auditor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.usuario.username         
    

#

class Secuencias(models.Model):
    nombre=models.CharField(max_length=250, verbose_name="Nombre",  null=False, blank=False)
    fecha_Inicio=models.DateTimeField(verbose_name="Fecha de Inicio", null=False, blank=False)
    fecha_Final=models.DateTimeField(verbose_name="Fecha de Finalización", null=True, blank=True)
    protocolo=models.ForeignKey(to=Protocolos, on_delete=models.CASCADE, verbose_name="Protocolo", null=True, blank=True)
    protocolo_proceso=models.ForeignKey(to=Proceso, on_delete=models.CASCADE, verbose_name="Protocolo de Proceso", null=True, blank=True)
    sistema=models.ForeignKey(to=Sistema, on_delete=models.CASCADE, verbose_name="Sistema", null=True, blank=False, related_name="sistema_nombre")
    class Status(models.TextChoices):
        REGISTRADA = "Registrada", "REGISTRADA"
        INVALIDA = "Invalida", "INVALIDA"
        REVISADA = "Revisada", "REVISADA"
        IMPRESA = "Impresa", "IMPRESA"
        REPORTADA = "Reportada", "REPORTADA"
        AUDITADA = "Auditada", "AUDITADA"
        ENSAYO = "Ensayo", "ENSAYO"
    status=models.CharField(max_length=90, choices=Status.choices, default=Status.REGISTRADA, verbose_name="Status", null=True, blank=True)  
    class Invalidar_Secuencia(models.TextChoices):
        PROBLEMAS_EQUIPO_1 = "Problemas de equipo (Equipo presionado, Linea base defectuosa)", "PROBLEMAS_EQUIPO_1"
        PROBLEMAS_EQUIPO_2 = "Problemas de equipo (Otros: Caidas de presión, Picos fantasmas; Problemas de software/hadware...)", "PROBLEMAS_EQUIPO_2"
        PROBLEMAS_COLUMNA = "Problemas de columna", "PROBLEMAS_COLUMNA"
        INCUMPLIMIENTO_SST_1 = "Incumplimiento de System (RSD)", "INCUMPLIMIENTO_SST_1"
        INCUMPLIMIENTO_SST_2 = "Incumplimiento de System (Otros: Resolución, Asimetria, Platos teóricos, Señal ruido)", "INCUMPLIMIENTO_SST_2"
        INCUMPLIMIENTO_SST_3 = "Incumplimiento de System (Correlación)", "INCUMPLIMIENTO_SST_3"
        PROBLEMAS_FM = "Problemas de Fases Móviles (TR Corridos, FM saturada, Otros...)", "PROBLEMAS_DE_FASE_MOVIL"
        PROBLEMAS_RED = "Problemas de red", "PROBLEMAS_RED"
        PROBLEMAS_FE = "Fallas de Fluido Eléctrico", "PROBLEMAS_DE_FLUIDO_ELECTRICO"
        OTROS = "Otros (definir en observaciones)", "OTROS"
    invalidar_Secuencia=models.CharField(max_length=250, choices=Invalidar_Secuencia.choices, verbose_name="Invalidar Secuencia", null=True, blank=True)  
    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion", null=True, blank=True)  
    observaciones=models.CharField(max_length=250, verbose_name="Observaciones",  null=True, blank=True)
    parametro_sq=models.ForeignKey(to=Parametro, on_delete=models.CASCADE, verbose_name="Parametro", null=True, blank=True)
    metodo=models.ForeignKey(to=Metodo, on_delete=models.CASCADE, verbose_name="Metodo", null=True, blank=True)
    muestras=models.ForeignKey(to=Muestras_y_Placebos, on_delete=models.CASCADE, verbose_name="Muestras", null=True, blank=True)
    fecha_invalidar=models.DateTimeField(verbose_name="Fecha de Invalidéz", null=True, blank=True)
    fecha_configuracion_protocolo_metodo=models.DateTimeField(verbose_name="Fecha Configuracion Protocolo de Metodo", null=True, blank=True)
    fecha_configuracion_protocolo_proceso=models.DateTimeField(verbose_name="Fecha Configuracion Protocolo de Proceso", null=True, blank=True)
    fecha_registro=models.DateTimeField(verbose_name="Fecha de Registro", null=True, blank=True)
    fecha_validar=models.DateTimeField(verbose_name="Fecha de Validación", null=True, blank=True)
    fecha_impresion=models.DateTimeField(verbose_name="Fecha de Impresión", null=True, blank=True)
    fecha_reporte=models.DateTimeField(verbose_name="Fecha de Reporte", null=True, blank=True)
    fecha_auditada=models.DateTimeField(verbose_name="Fecha auditada", null=True, blank=True)
    def individual():
     " This function will be called when a default value is needed.ll return a 31 length string with a-z, 0-9."
     return 'Prueba'
    invalidar=models.CharField(max_length=250, verbose_name="Invalidada por",  null=True, blank=True)
    registrada_por=models.CharField(max_length=250, verbose_name="Registrada por",  null=True, blank=True)
    validar=models.CharField(max_length=250, verbose_name="Validada por",  null=True, blank=True)
    imprimir=models.CharField(max_length=250, verbose_name="Impresa",  null=True, blank=True)
    reportar=models.CharField(max_length=250, verbose_name="Reportada por",  null=True, blank=True)
    auditar=models.CharField(max_length=250, verbose_name="Auditada por",  null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['protocolo', 'parametro_sq', 'fecha_configuracion_protocolo_metodo'], name='unique'),
            models.UniqueConstraint(fields=['protocolo_proceso', 'muestras', 'fecha_configuracion_protocolo_proceso'], name='unique_intro_nue'),
        ]
    def nombre_Secuencia(self):
        return "{}".format(self.nombre)    
    def __str__(self):    

        return str(self.nombre_Secuencia())
  
class Lavado_buzo(models.Model):
    sistema=models.ForeignKey(to=Sistema, on_delete=models.CASCADE, verbose_name="Sistema", null=True, blank=False)
    fecha_lavado_buzo=models.DateField(verbose_name="Fecha de lavado de buzos", null=True, blank=True)
    fecha_lavado_celda=models.DateField(verbose_name="Fecha de lavado de celda", null=True, blank=True)
    fecha_test_diagnostico=models.DateField(verbose_name="Fecha del test", null=True, blank=True)
    fecha_mantenimiento=models.DateField(verbose_name="Fecha del Mantenimiento", null=True, blank=True) 
    fecha_calificacion=models.DateField(verbose_name="Fecha de la calificación", null=True, blank=True) 
    fecha_alerta_inferior=models.DateField(verbose_name="Fecha de alerta inferior", null=True, blank=True)
    fecha_alerta_superior=models.DateField(verbose_name="Fecha de alerta superior", null=True, blank=True)
    fecha_alerta_inferior_celda=models.DateField(verbose_name="Fecha de alerta inferior celda", null=True, blank=True)
    fecha_alerta_superior_celda=models.DateField(verbose_name="Fecha de alerta superior celda", null=True, blank=True)
    fecha_alerta_inferior_test=models.DateField(verbose_name="Fecha de alerta inferior test", null=True, blank=True)
    fecha_alerta_superior_test=models.DateField(verbose_name="Fecha de alerta superior test", null=True, blank=True) 
    fecha_alerta_inferior_mantenimiento=models.DateField(verbose_name="Fecha de alerta inferior mantenimiento", null=True, blank=True) 
    fecha_alerta_superior_mantenimiento=models.DateField(verbose_name="Fecha de alerta superior mantenimiento", null=True, blank=True) 
    fecha_alerta_inferior_calificacion=models.DateField(verbose_name="Fecha de alerta inferior calificación", null=True, blank=True) 
    fecha_alerta_superior_calificacion=models.DateField(verbose_name="Fecha de alerta superior calificación", null=True, blank=True) 

    class Condicion(models.TextChoices):
        ACTIVO = "Activo", "ACTIVO"
        PASIVO = "Pasivo", "PASIVO"
    condicion=models.CharField(max_length=90, choices=Condicion.choices, default=Condicion.ACTIVO, verbose_name="Condicion") 
    class Status(models.TextChoices):
        PROGRAMADO = "Programado", "PROGRAMADO"
        REALIZADO = "Realizado", "REALIZADO"
        PENDIENTE = "Pendiente", "PENDIENTE"
    status=models.CharField(max_length=90, choices=Status.choices, default=Status.PROGRAMADO, verbose_name="Status Buzos", null=True, blank=True)
    class Status_celda(models.TextChoices):
        PROGRAMADO = "Programado", "PROGRAMADO"
        REALIZADO = "Realizado", "REALIZADO"
        PENDIENTE = "Pendiente", "PENDIENTE"
    status_celda=models.CharField(max_length=90, choices=Status_celda.choices, default=Status_celda.PROGRAMADO, verbose_name="Status Celdas", null=True, blank=True)

    class Status_test(models.TextChoices): 
        PROGRAMADO = "Programado", "PROGRAMADO"
        REALIZADO = "Realizado", "REALIZADO"
        PENDIENTE = "Pendiente", "PENDIENTE"
    status_test=models.CharField(max_length=90, choices=Status_test.choices, default=Status_test.PROGRAMADO, verbose_name="Status Test", null=True, blank=True)

    class Status_mantenimiento(models.TextChoices): 
        PROGRAMADO = "Programado", "PROGRAMADO"
        REALIZADO = "Realizado", "REALIZADO"
        PENDIENTE = "Pendiente", "PENDIENTE"
    status_mantenimiento=models.CharField(max_length=90, choices=Status_mantenimiento.choices, default=Status_mantenimiento.PROGRAMADO, verbose_name="Status Mantenimiento", null=True, blank=True)

    class Status_calificacion(models.TextChoices): 
        PROGRAMADO = "Programado", "PROGRAMADO"
        REALIZADO = "Realizado", "REALIZADO"
        PENDIENTE = "Pendiente", "PENDIENTE"
    status_calificacion=models.CharField(max_length=90, choices=Status_calificacion.choices, default=Status_calificacion.PROGRAMADO, verbose_name="Status Calificación", null=True, blank=True) 
    realizado_por=models.CharField(max_length=250, verbose_name="Lavado de buzos realizados por",  null=True, blank=True)
    realizado_por_celda=models.CharField(max_length=250, verbose_name="Lavado de celda realizado por",  null=True, blank=True)

    realizado_por_test=models.CharField(max_length=250, verbose_name="Test realizado por",  null=True, blank=True)

    realizado_por_mantenimiento=models.CharField(max_length=250, verbose_name="Mantenimiento realizado por",  null=True, blank=True) 

    realizado_por_calificacion=models.CharField(max_length=250, verbose_name="Calificado por",  null=True, blank=True)
    
    observaciones=models.CharField(max_length=250, verbose_name="Observaciones",  null=True, blank=True)
    def __str__(self):    
        return str(self.sistema)  
    











