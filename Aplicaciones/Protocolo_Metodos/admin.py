from django.contrib import admin


from django.contrib import admin
from .models import Ensayo
from .models import EstadoProtocolo
from .models import Metodologia
from .models import Subparametro
from .models import Titulo_Parametro
from .models import Parametro
from .models import Viabilidad
from .models import Muestras_y_Placebos
from .models import Protocolos
from .models import Cliente
from .models import Celda
from .models import Tipo_muestra
from .models import Etapa
from .models import Metodo

#admin.site.site_header = "monsterApp"

#admin.site.site_title = "Sistema Analítico MonserApp"
#admin.site.index_title = "Portal de administración MonsterApp"


# Register your models here.

class EnsayoAdmin(admin.ModelAdmin):
    search_fields = ("nombre_ensayo"),
    list_display = ["id", "nombre_ensayo"]

class CeldaAdmin(admin.ModelAdmin):
    search_fields = ("nombre_celda"),
    list_display = ["id", "nombre_celda", "responsable"]    

class ParametroAdmin(admin.ModelAdmin):
    search_fields = ("id"),
    list_display = ["id", "nombre_Parametro"]

class TituloParametroAdmin(admin.ModelAdmin):
    search_fields = ("titulo_parametro"),
    list_display = ["id", "titulo_parametro"]

class SubparametroParametroAdmin(admin.ModelAdmin):
    search_fields = ("nombre_subparametro"),
    list_display = ["id", "nombre_subparametro"]    

class MuestrasAdmin(admin.ModelAdmin):
    search_fields = ("codigo_muestra_interno"),
    list_display = ["id", "codigo_muestra_interno","nombre_muestra", "codigo_muestra_producto", "lote_muestra"]

class ClienteAdmin(admin.ModelAdmin):
    search_fields = ("nombre_cliente"),
    list_display = ["id","nombre_cliente"]

class MetodologiaAdmin(admin.ModelAdmin):
    search_fields = ("nombre_metodologia"),
    list_display = ["id","nombre_metodologia"]

class ProtocolosAdmin(admin.ModelAdmin):
    #autocomplete_fields = ["metodologia", "cliente"]
    search_fields = ("nombre"),
    list_display=["id","codigo","nombre","ensayo","metodologia","cliente","estado_protocolo","observaciones"]

class MetodoAdmin(admin.ModelAdmin):
    search_fields = ("codigo_metodo"),
    list_display = ["id","codigo_metodo", "nombre_metodo" ]

 


  

admin.site.register(Ensayo, EnsayoAdmin)
admin.site.register(EstadoProtocolo)
admin.site.register(Metodologia, MetodologiaAdmin)
admin.site.register(Subparametro, SubparametroParametroAdmin)
admin.site.register(Titulo_Parametro, TituloParametroAdmin)
admin.site.register(Parametro, ParametroAdmin)
admin.site.register(Viabilidad)
admin.site.register(Muestras_y_Placebos, MuestrasAdmin)
admin.site.register(Protocolos, ProtocolosAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Celda, CeldaAdmin)
admin.site.register(Tipo_muestra)
admin.site.register(Etapa)
admin.site.register(Metodo, MetodoAdmin)



