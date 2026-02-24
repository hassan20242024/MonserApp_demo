
from ..models import Secuencias,Muestras_y_Placebos, Protocolos, Parametro, Sistema
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import datetime
from django.utils import formats
from django.http import JsonResponse, HttpResponse
from dateutil.relativedelta import relativedelta, MO
from django.core import serializers


@login_required
def listado_secuencias_registradas(request):
    listado_secuencias = Secuencias.objects.filter(status="Registrada")
    if (len(listado_secuencias) > 0 ):
     datos = []
     for secuencias in listado_secuencias:
        listado_muestras_metodo = secuencias.protocolo
        listado_muestras_ = secuencias.protocolo
        if listado_muestras_metodo is not None:
          if listado_muestras_metodo.muestras_y_Placebos.all() is not None:
            datos.append(
              {
            "id": secuencias.pk,
            "nombre": secuencias.nombre,
            "status": secuencias.status,
            "sistema": secuencias.sistema.nombre,
            "observaciones": secuencias.observaciones,
            "protocolo": str(secuencias.protocolo),
            "protocolo_proceso": str(secuencias.protocolo_proceso),
            "metodo": str(secuencias.metodo),
            "parametro": str(secuencias.parametro_sq),
             "descripcion": (list(listado_muestras_metodo.muestras_y_Placebos.values_list("nombre_muestra", "lote_muestra", "codigo_muestra_producto", "codigo_muestra_interno"))),
             "registrada_por": secuencias.registrada_por,
             "validada_por": secuencias.validar,
             "impresa_por": secuencias.imprimir,
              "reportada_por": secuencias.reportar,
              "auditada_por": secuencias.auditar,
            "fecha_registro": str(secuencias.fecha_registro),
            "fecha_validacion": str(secuencias.fecha_validar),
              "fecha_impresion": str(secuencias.fecha_impresion),
              "fecha_reporte": str(secuencias.fecha_reporte),
              "fecha_auditoria": str( secuencias.fecha_auditada)
        }
        )
        else:
          datos.append(
              
              {
            "id": secuencias.pk,
            "nombre": secuencias.nombre,
            "status": secuencias.status,
            "sistema": secuencias.sistema.nombre,
            "observaciones": secuencias.observaciones,
            "protocolo": str(secuencias.protocolo),
            "protocolo_proceso": str(secuencias.protocolo_proceso),
            "metodo": str(secuencias.metodo),
            "parametro": str(secuencias.parametro_sq),
             "registrada_por": secuencias.registrada_por,
              "validada_por": secuencias.validar,
              "impresa_por": secuencias.imprimir,
              "reportada_por": secuencias.reportar,
              "auditada_por": secuencias.auditar,
              "fecha_validacion": str(secuencias.fecha_validar),
            "fecha_registro": str(secuencias.fecha_registro),
              "fecha_impresion": str(secuencias.fecha_impresion),
              "fecha_reporte": str(secuencias.fecha_reporte),
              "fecha_auditoria": str( secuencias.fecha_auditada),
            "muestra_proceso": {
                "nombre": str(secuencias.muestras.nombre_muestra),
                "lote": str(secuencias.muestras.lote_muestra),
                "codigo_producto": str(secuencias.muestras.codigo_muestra_producto),
                "etapa": str(secuencias.muestras.etapa),
            }
        }
        )
         
     datos_json = json.dumps(datos)
     response = HttpResponse(datos_json, content_type="application/json")
    else:
     datos_json = {"message": "Not Found"} 
    return response

@login_required
def listado_secuencias_validadas(request):
    listado_secuencias = Secuencias.objects.filter(~Q(status__in=["Registrada", "Invalida"]))
    if (len(listado_secuencias) > 0 ):
     datos = []
     for secuencias in listado_secuencias:
        listado_muestras_metodo = secuencias.protocolo
        listado_muestras_ = secuencias.protocolo
        if listado_muestras_metodo is not None:
          if listado_muestras_metodo.muestras_y_Placebos.all() is not None:
            datos.append(
              {
            "id": secuencias.pk,
            "nombre": secuencias.nombre,
            "status": secuencias.status,
            "sistema": secuencias.sistema.nombre,
            "observaciones": secuencias.observaciones,
            "protocolo": str(secuencias.protocolo),
            "protocolo_proceso": str(secuencias.protocolo_proceso),
            "metodo": str(secuencias.metodo),
            "parametro": str(secuencias.parametro_sq),
             "descripcion": (list(listado_muestras_metodo.muestras_y_Placebos.values_list("nombre_muestra", "lote_muestra", "codigo_muestra_producto", "codigo_muestra_interno"))),
             "registrada_por": secuencias.registrada_por,
             "validada_por": secuencias.validar,
             "impresa_por": secuencias.imprimir,
              "reportada_por": secuencias.reportar,
              "auditada_por": secuencias.auditar,
            "fecha_registro": str(secuencias.fecha_registro),
            "fecha_validacion": str(secuencias.fecha_validar),
              "fecha_impresion": str(secuencias.fecha_impresion),
              "fecha_reporte": str(secuencias.fecha_reporte),
              "fecha_auditoria": str( secuencias.fecha_auditada)
        }
        )
        else:
          datos.append(
              {
            "id": secuencias.pk,
            "nombre": secuencias.nombre,
            "status": secuencias.status,
            "sistema": secuencias.sistema.nombre,
            "observaciones": secuencias.observaciones,
            "protocolo": str(secuencias.protocolo),
            "protocolo_proceso": str(secuencias.protocolo_proceso),
            "metodo": str(secuencias.metodo),
            "parametro": str(secuencias.parametro_sq),
             "registrada_por": secuencias.registrada_por,
              "validada_por": secuencias.validar,
              "impresa_por": secuencias.imprimir,
              "reportada_por": secuencias.reportar,
              "auditada_por": secuencias.auditar,
            "fecha_registro": str(secuencias.fecha_registro),
            "fecha_validacion": str(secuencias.fecha_validar),
              "fecha_impresion": str(secuencias.fecha_impresion),
              "fecha_reporte": str(secuencias.fecha_reporte),
              "fecha_auditoria": str( secuencias.fecha_auditada),
            "muestra_proceso": {
                "nombre": str(secuencias.muestras.nombre_muestra),
                "lote": str(secuencias.muestras.lote_muestra),
                "codigo_producto": str(secuencias.muestras.codigo_muestra_producto),
                "etapa": str(secuencias.muestras.etapa),
            }
        }
        )
         
     datos_json = json.dumps(datos)
     response = HttpResponse(datos_json, content_type="application/json")
    else:
     datos_json = {"message": "Not Found"} 
    return response

@login_required
def listado_secuencias_invalidas(request):
    listado_secuencias = Secuencias.objects.filter(status="Invalida")
    if (len(listado_secuencias) > 0 ):
     datos = []
     for secuencias in listado_secuencias:
        listado_muestras_metodo = secuencias.protocolo
        listado_muestras_ = secuencias.protocolo
        if listado_muestras_metodo is not None:
          if listado_muestras_metodo.muestras_y_Placebos.all() is not None:
            datos.append(
              {
            "id": secuencias.pk,
            "nombre": secuencias.nombre,
            "status": secuencias.status,
            "sistema": secuencias.sistema.nombre,
            "invalidar_Secuencia": secuencias.invalidar_Secuencia,
            "observaciones": secuencias.observaciones,
            "protocolo": str(secuencias.protocolo),
            "protocolo_proceso": str(secuencias.protocolo_proceso),
            "metodo": str(secuencias.metodo),
            "parametro": str(secuencias.parametro_sq),
             "descripcion": (list(listado_muestras_metodo.muestras_y_Placebos.values_list("nombre_muestra", "lote_muestra", "codigo_muestra_producto", "codigo_muestra_interno"))),
             "registrada_por": secuencias.registrada_por,
             "invalidada_por": secuencias.invalidar,
            "fecha_registro": str(secuencias.fecha_registro),
            "fecha_invalidez": str(secuencias.fecha_invalidar),
        }
        )
        else:
          datos.append(
              
              {
            "id": secuencias.pk,
            "nombre": secuencias.nombre,
            "status": secuencias.status,
            "sistema": secuencias.sistema.nombre,
            "invalidar_Secuencia": secuencias.invalidar_Secuencia,
            "observaciones": secuencias.observaciones,
            "protocolo": str(secuencias.protocolo),
            "protocolo_proceso": str(secuencias.protocolo_proceso),
            "metodo": str(secuencias.metodo),
            "parametro": str(secuencias.parametro_sq),
             "registrada_por": secuencias.registrada_por,
              "invalidada_por": secuencias.invalidar,
            "fecha_registro": str(secuencias.fecha_registro),
           "fecha_invalidez": str(secuencias.fecha_invalidar),
            "muestra_proceso": {
                "nombre": str(secuencias.muestras.nombre_muestra),
                "lote": str(secuencias.muestras.lote_muestra),
                "codigo_producto": str(secuencias.muestras.codigo_muestra_producto),
                "etapa": str(secuencias.muestras.etapa),
            }
        }
        )
         
     datos_json = json.dumps(datos)
     response = HttpResponse(datos_json, content_type="application/json")
    else:
     datos_json = {"message": "Not Found"} 
    return response

@login_required
def listado_protocolos_metodos(request):
    protocolos_metodos = list(Protocolos.objects.values())
    if (len(protocolos_metodos) > 0 ):
        data = {"message": "Success", "protocolos_metodos": protocolos_metodos} 
    else:
        data = {"message": "Not Found"} 
    return JsonResponse(data) 

@login_required
def listado_parametros(request):
    parametros = list(Parametro.objects.values())
    if (len(parametros) > 0 ):
        data = {"message": "Success", "parametros": parametros} 
    else:
        data = {"message": "Not Found"} 
    return JsonResponse(data) 

@login_required
def listado_parametros_por_id(request, pk):
    parametros = list(Parametro.objects.filter(pk = pk).values())
    if (len(parametros) > 0 ):
        data = {"message": "Success", "parametros": parametros} 
    else:
        data = {"message": "Not Found"} 
    return JsonResponse(data)

@login_required
def listado_sistemas(request):
    sistemas = list(Sistema.objects.values())
    if (len(sistemas) > 0 ):
        data = {"message": "Success", "sistemas": sistemas} 
    else:
        data = {"message": "Not Found"} 
    return JsonResponse(data)  

@login_required
def listado_muestras(request):
    muestras_qs = Muestras_y_Placebos.objects.select_related('etapa__ensayo')
    
    muestras = []
    for m in muestras_qs:
        muestras.append({
            "id": m.id,
            "nombre_muestra": m.nombre_muestra,
            "lote_muestra": m.lote_muestra,
            "codigo_muestra_interno": m.codigo_muestra_interno,
            "codigo_muestra_producto": m.codigo_muestra_producto,
            "etapa_id": m.etapa.id if m.etapa else None,
            "etapa_nombre": m.etapa.nombre_etapa if m.etapa else None,
            "ensayo_nombre": m.etapa.ensayo.nombre_ensayo if m.etapa and m.etapa.ensayo else None,
        })

    if muestras:
        return JsonResponse({"message": "Success", "muestras": muestras})
    else:
        return JsonResponse({"message": "Not Found", "muestras": []})
