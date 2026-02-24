from django.shortcuts import render, redirect, get_object_or_404
from ..models import Secuencias,Proceso,Muestras_y_Placebos, Protocolos, Parametro,Metodo, Ensayo, Sistema, Perfil,usuario_invalidar,usuario_validar, usuario_reporte,usuario_impresion,usuario_auditor,Lavado_buzo
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q
import json
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import datetime
from django.utils import timezone, formats
from django.http import JsonResponse, HttpResponse
from dateutil.relativedelta import relativedelta, MO
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now 
from django.db import IntegrityError
import traceback
from django.views.decorators.csrf import csrf_exempt


@login_required
def proceso_secuencias_en_curso(request):
    secuenicas=Secuencias.objects.all()
    protocolos=Protocolos.objects.all()
    protocolo_proceso =Proceso.objects.all()
    muestras=Muestras_y_Placebos.objects.all()
    metodo=Metodo.objects.all()
    parametros=Parametro.objects.all()
    ensayo=Ensayo.objects.all()
    sistema=Sistema.objects.all()
    invalidar=usuario_invalidar.objects.filter(usuario=request.user)
    validar=usuario_validar.objects.filter(usuario=request.user)
    imprimir=usuario_impresion.objects.filter(usuario=request.user)
    reportar=usuario_reporte.objects.filter(usuario=request.user)
    auditar=usuario_auditor.objects.filter(usuario=request.user)
    usuarios=Perfil.objects.all()
    secuencia=Secuencias.objects.all()
    super_usuario=Perfil.objects.all()
        
    context={
        "invalidar":invalidar,
        "validar":validar,
        "secuenicas":secuenicas,
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "reportar":reportar,
         "secuencia":secuencia,
         "super_usuario":super_usuario,
        "auditar":auditar,
         "imprimir":imprimir,
         "usuarios":usuarios,
         "protocolo_proceso":protocolo_proceso,
         "muestras":muestras,
         "metodo":metodo,
    }
    return render(request, "secuencias/proceso_secuencias_en_curso.html", context)

@login_required
def registro_inicial_de_secuencias(request):
    secuenicas=Secuencias.objects.all()
    protocolos=Protocolos.objects.all()
    protocolo_proceso =Proceso.objects.all()
    muestras=Muestras_y_Placebos.objects.all()
    metodo=Metodo.objects.all()
    parametros=Parametro.objects.all()
    ensayo=Ensayo.objects.all()
    sistema=Sistema.objects.all()
    invalidar=usuario_invalidar.objects.filter(usuario=request.user)
    validar=usuario_validar.objects.filter(usuario=request.user)
    imprimir=usuario_impresion.objects.filter(usuario=request.user)
    reportar=usuario_reporte.objects.filter(usuario=request.user)
    auditar=usuario_auditor.objects.filter(usuario=request.user)
    usuarios=Perfil.objects.all()
    secuencia=Secuencias.objects.all()
    super_usuario=Perfil.objects.all()
        
    context={
        "invalidar":invalidar,
        "validar":validar,
        "secuenicas":secuenicas,
        "protocolos":protocolos,
        "parametros":parametros,
         "ensayo":ensayo,
         "sistema":sistema,
         "reportar":reportar,
         "secuencia":secuencia,
         "super_usuario":super_usuario,
        "auditar":auditar,
         "imprimir":imprimir,
         "usuarios":usuarios,
         "protocolo_proceso":protocolo_proceso,
         "muestras":muestras,
         "metodo":metodo,
    }
    return render(request, "secuencias/registro_inicial_de_secuencias.html", context)


@login_required
def chart_js_proceso_secuencias_en_curso(request):
    return render(request, 'secuencias/chart_js__proceso_secuencias_en_curso.html')

@login_required
def chart_data_json(request):
    registro_total = Secuencias.objects.count()
    pendientes_validaciones = Secuencias.objects.filter(status="Registrada").count()
    pendientes_impresiones = Secuencias.objects.filter(status="Revisada").count()
    pendientes_reportes = Secuencias.objects.filter(status="Impresa").count()
    pendientes_auditorias = Secuencias.objects.filter(status="Reportada").count()
    invalidas = Secuencias.objects.filter(status="Invalida").count()
    ensayos = Secuencias.objects.filter(status="Ensayo").count()

    total_grafico_pie_secuencias = pendientes_validaciones + pendientes_impresiones + pendientes_reportes + pendientes_auditorias
    divisor = total_grafico_pie_secuencias if total_grafico_pie_secuencias > 0 else 1

    procentaje_pendientes_validaciones = pendientes_validaciones * 100 / divisor
    procentaje_pendientes_impresiones = pendientes_impresiones * 100 / divisor
    procentaje_pendientes_reportes = pendientes_reportes * 100 / divisor
    procentaje_pendientes_auditorias = pendientes_auditorias * 100 / divisor

    # Datos para gráficos y series (simplifico la estructura igual que en tu función original)
    pendiente_validacion = pendientes_validaciones
    pendiente_impresion = pendientes_impresiones
    pendiente_reporte = pendientes_reportes
    pendientes_auditoria = pendientes_auditorias

    chart1 = {
        'chart': {'type': 'pie'},
        'title': {'text': ''},
        "credits": "false",
        "plotOptions": {
            "pie": {
                "pointPadding": 0,
                "borderWidth": 8,
            }
        },
        'series': [{
            "name": "Status",
            'data': [
                {'y': pendiente_validacion, 'name': f'{int(procentaje_pendientes_validaciones)}% Adquiriendo', 'color': "#95a5a6"},
                {'y': pendiente_impresion, 'name': f'{int(procentaje_pendientes_impresiones)}% Impresiones pendientes', 'color': "#1abc9c"},
                {'y': pendiente_reporte, 'name': f'{int(procentaje_pendientes_reportes)}% Reportes pendientes', 'color': "#9b59b6"},
                {'y': pendientes_auditoria, 'name': f'{int(procentaje_pendientes_auditorias)}% Pendientes por auditar', 'color': "#3498db"},
            ]
        }]
    }

    chart1A = {
        'chart': {'type': 'column'},
        'title': {'text': ''},
        "credits": "false",
        "xAxis": {
            "categories": ['Adquiriendo', 'Impresiones pendientes', 'Reportes pendientes', 'Pendientes por auditar']
        },
        "plotOptions": {
            "column": {
                "pointPadding": 0.2,
                "borderWidth": 15,
            }
        },
        'series': [{
            "name": "Status",
            'data': [
                {'y': pendiente_validacion, 'name': "Adquiriendo", 'color': "#95a5a6"},
                {'y': pendiente_impresion, 'name': "Impresiones pendientes", 'color': "#1abc9c"},
                {'y': pendiente_reporte, 'name': "Reportes pendientes", 'color': "#9b59b6"},
                {'y': pendientes_auditoria, 'name': "Pendientes por auditar", 'color': "#3498db"},
            ]
        }]
    }

    dataset = Secuencias.objects.values('sistema__nombre') \
        .annotate(
            registrada=Count('sistema', filter=Q(status="Registrada")),
            validada=Count('sistema', filter=Q(status="Revisada")),
            impresa=Count('sistema', filter=Q(status="Impresa"))
        ).order_by('-sistema__nombre')

    categories = []
    registrada = []
    validada = []
    impresa = []

    for entry in dataset:
        categories.append(entry['sistema__nombre'])
        registrada.append(entry['registrada'])
        validada.append(entry['validada'])
        impresa.append(entry['impresa'])

    registrada_series = {'name': 'Adquiriendo', 'data': registrada, 'color': "#95a5a6"}
    validada_series = {'name': 'Impresiones pendientes', 'data': validada, 'color': "#1abc9c"}
    impresa_series = {'name': 'Reportes pendientes', 'data': impresa, 'color': "#9b59b6"}

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': ''},
        "credits": "false",
        'xAxis': {'categories': categories},
        'series': [registrada_series, validada_series, impresa_series],
    }

    return JsonResponse({
        "registro_total": registro_total,
        "pendientes_validaciones": pendientes_validaciones,
        "pendientes_impresiones": pendientes_impresiones,
        "pendientes_reportes": pendientes_reportes,
        "invalidas": invalidas,
        "ensayos": ensayos,
        "pendientes_auditorias": pendientes_auditorias,
        "chart": chart,
        "chart1": chart1,
        "chart1A": chart1A,
    })



@login_required
def retornar_estado_registrada(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            secuencias = data.get("secuencias", [])

            now = datetime.datetime.now()
            cero = "0001-01-01"
            user = str(request.user)

            for item in secuencias:
                id = item.get("id")
                tipo = item.get("tipo")

                secuencia = Secuencias.objects.get(pk=id)
                secuencia.status = Secuencias.Status.REGISTRADA
                secuencia.invalidar_Secuencia = None
                secuencia.fecha_invalidar = None
                secuencia.invalidar = None

                if tipo == "protocolo_metodo":
                    secuencia.fecha_configuracion_protocolo_metodo = cero
                    secuencia.fecha_configuracion_protocolo_proceso = now
                elif tipo == "protocolo_proceso":
                    secuencia.fecha_configuracion_protocolo_metodo = now
                    secuencia.fecha_configuracion_protocolo_proceso = cero
                elif tipo == "otro":
                    secuencia.fecha_configuracion_protocolo_metodo = now
                    secuencia.fecha_configuracion_protocolo_proceso = now

                try:
                    secuencia.save()
                except IntegrityError as e:
                    if "unique" in str(e).lower():
                        return JsonResponse({
                            "success": False,
                            "message": "Una o más secuencias ya están registradas con los mismos datos únicos. Verifica combinaciones duplicadas."
                        }, status=400)
                    else:
                        raise  # Re-lanza si no es error de unicidad

            return JsonResponse({
                "success": True,
                "message": "Registros revisados correctamente",
                "ids_actualizados": [item["id"] for item in secuencias]
            })

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error general: {str(e)}"}, status=400)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

@login_required
def secuencias_invalidadas(request):
    secuencias=Secuencias.objects.all()
    validar=usuario_validar.objects.filter(usuario=request.user)
        
    context={
        "secuencias":secuencias,
        "validar":validar
    }
    return render(request, "secuencias/secuencias_invalidadas.html", context)

@login_required
def cambiar_estado_revisar(request):
    data = json.loads(request.body)
    ids = data.get("ids", [])
    nuevo_estado = data.get("status", Secuencias.Status.REVISADA)
    revisada_por = data.get("validar", str(User.objects.get(username=request.user)))
    fecha_revision = data.get("fecha_validar", datetime.datetime.now())
    Secuencias.objects.filter(id__in=ids).update(status=nuevo_estado, validar=revisada_por, fecha_validar=fecha_revision)
    return JsonResponse({"success": True, "ids_actualizados": ids})

@login_required
def cambiar_estado_reportar(request):
    data = json.loads(request.body)
    ids = data.get("ids", [])
    nuevo_estado = data.get("status", Secuencias.Status.REPORTADA)
    reportada_por = data.get("reportar", str(User.objects.get(username=request.user)))
    fecha_reporte = data.get("fecha_reporte", datetime.datetime.now())
    Secuencias.objects.filter(id__in=ids).update(status=nuevo_estado, reportar=reportada_por, fecha_reporte=fecha_reporte)
    return JsonResponse({"success": True, "ids_actualizados": ids})

@login_required
def cambiar_estado_impresa(request):
    data = json.loads(request.body)
    ids = data.get("ids", [])
    nuevo_estado = data.get("status", Secuencias.Status.IMPRESA)
    impresa_por = data.get("imprimir", str(User.objects.get(username=request.user)))
    fecha_impresion = data.get("fecha_impresion", datetime.datetime.now())
    Secuencias.objects.filter(id__in=ids).update(status=nuevo_estado, imprimir=impresa_por, fecha_impresion=fecha_impresion)
    return JsonResponse({"success": True, "ids_actualizados": ids})

@login_required
def cambiar_estado_auditada(request):
    data = json.loads(request.body)
    ids = data.get("ids", [])
    nuevo_estado = data.get("status", Secuencias.Status.AUDITADA)
    auditada_por = data.get("auditar", str(User.objects.get(username=request.user)))
    fecha_auditada = data.get("fecha_auditada", datetime.datetime.now())
    Secuencias.objects.filter(id__in=ids).update(status=nuevo_estado, auditar=auditada_por, fecha_auditada=fecha_auditada)
    return JsonResponse({"success": True, "ids_actualizados": ids})

def es_administrador(user):
    return user.groups.filter(name="Administrador").exists()

@login_required
def revertir_estado_a_reportada(request):
    data = json.loads(request.body)
    ids = data.get("ids", [])
    nuevo_estado = data.get("status", Secuencias.Status.AUDITADA)
    usuario = request.user
    ahora = datetime.datetime.now()
    # Si se reporta (avance) o retrocede desde Auditada
    if nuevo_estado == Secuencias.Status.AUDITADA:
        Secuencias.objects.filter(id__in=ids).update(
            status=nuevo_estado,
            auditar=str(usuario),
            fecha_auditada=ahora
        )
    elif nuevo_estado == Secuencias.Status.REPORTADA and es_administrador(usuario):
        # Retroceder de Reportada → Impresa
        Secuencias.objects.filter(id__in=ids).update(
            status=nuevo_estado,
            auditar=None,
            fecha_auditada=None
        )
    return JsonResponse({"success": True, "ids_actualizados": ids})

@login_required
def revertir_estado_a_impresa(request):
    data = json.loads(request.body)
    ids = data.get("ids", [])
    nuevo_estado = data.get("status", Secuencias.Status.REPORTADA)
    usuario = request.user
    ahora = datetime.datetime.now()
    # Si se reporta (avance) o retrocede desde Auditada
    if nuevo_estado == Secuencias.Status.REPORTADA:
        Secuencias.objects.filter(id__in=ids).update(
            status=nuevo_estado,
            reportar=str(usuario),
            fecha_reporte=ahora
        )
    elif nuevo_estado == Secuencias.Status.IMPRESA and es_administrador(usuario):
        # Retroceder de Reportada → Impresa.
        Secuencias.objects.filter(id__in=ids).update(
            status=nuevo_estado,
            reportar=None,
            fecha_reporte=None
        )
    return JsonResponse({"success": True, "ids_actualizados": ids})

@login_required
def revertir_estado_a_revisada(request):
    data = json.loads(request.body)
    ids = data.get("ids", [])
    nuevo_estado = data.get("status", Secuencias.Status.IMPRESA)
    usuario = request.user
    ahora = datetime.datetime.now()
    # Si se reporta (avance) o retrocede desde Auditada
    if nuevo_estado == Secuencias.Status.IMPRESA:
        Secuencias.objects.filter(id__in=ids).update(
            status=nuevo_estado,
            imprimir=str(usuario),
            fecha_impresion=ahora
        )
    elif nuevo_estado == Secuencias.Status.REVISADA and es_administrador(usuario):
        # Retroceder de Reportada → Impresa
        Secuencias.objects.filter(id__in=ids).update(
            status=nuevo_estado,
            imprimir=None,
            fecha_impresion=None
        )
    return JsonResponse({"success": True, "ids_actualizados": ids})

@login_required
def revertir_estado_a_registrada(request):
    data = json.loads(request.body)
    ids = data.get("ids", [])
    nuevo_estado = data.get("status", Secuencias.Status.REVISADA)
    usuario = request.user
    ahora = datetime.datetime.now()
    # Si se reporta (avance) o retrocede desde Auditada
    if nuevo_estado == Secuencias.Status.REVISADA:
        Secuencias.objects.filter(id__in=ids).update(
            status=nuevo_estado,
            validar=str(usuario),
            fecha_validar=ahora
        )
    elif nuevo_estado == Secuencias.Status.REGISTRADA and es_administrador(usuario):
        # Retroceder de Reportada → Impresa
        Secuencias.objects.filter(id__in=ids).update(
            status=nuevo_estado,
            validar=None,
            fecha_validar=None
        )
    return JsonResponse({"success": True, "ids_actualizados": ids})

@login_required
def actualizar_secuencia(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            secuencia = Secuencias.objects.get(pk=pk)
            status = data.get("status")
            secuencia.status = status
            secuencia.observaciones = data.get("observaciones")
            secuencia.nombre = data.get("nombre")
            sistema_id = data.get("sistema")
            if sistema_id:
                secuencia.sistema = Sistema.objects.get(id=sistema_id)
            # Si el status es "Ensayo", actualiza fechas
            if status == "Ensayo":
                secuencia.fecha_configuracion_protocolo_metodo = now()
                secuencia.fecha_configuracion_protocolo_proceso = now()

            secuencia.save()
            return JsonResponse({"success": True})
        except Secuencias.DoesNotExist:
            return JsonResponse({"success": False, "error": "No existe"})
        except Sistema.DoesNotExist:
            return JsonResponse({"success": False, "error": "Sistema no válido"})
    return JsonResponse({"success": False, "error": "Método inválido"})

@login_required
def cambiar_estado_invalida(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

        secuencias_ids = data.get("ids", [])
        causa = data.get("causa", None)

        if not secuencias_ids or not causa:
            return JsonResponse({'success': False, 'error': 'Faltan datos'}, status=400)

        for secuencia_id in secuencias_ids:
            try:
                secuencia = Secuencias.objects.get(pk=secuencia_id)
                secuencia.status = Secuencias.Status.INVALIDA
                secuencia.invalidar = str(request.user)
                secuencia.invalidar_Secuencia = causa
                now = datetime.datetime.now()
                secuencia.fecha_invalidar = now
                secuencia.fecha_configuracion_protocolo_metodo = now
                secuencia.fecha_configuracion_protocolo_proceso = now
                secuencia.save()
            except Secuencias.DoesNotExist:
                continue  

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
def crear_secuencias_protocolo_metodo(request):
    if request.method == "POST":
        try:
            nombre = request.POST.get("nombre")
            fecha_inicio = request.POST.get("fecha_Inicio")
            fecha_Final = request.POST.get("fecha_Final")
            protocolo_id = request.POST.get("protocolo")
            protocolo_proceso_id = request.POST.get("protocolo_proceso")
            metodo_id = request.POST.get("metodo")

            selecciones = [bool(protocolo_id), bool(protocolo_proceso_id), bool(metodo_id)]
            if selecciones.count(True) == 0:
                return JsonResponse({"status": "error", "message": "Debe seleccionar uno: protocolo, protocolo de proceso o método."}, status=400)
            elif selecciones.count(True) > 1:
                return JsonResponse({"status": "error", "message": "Solo debe seleccionar uno entre: protocolo, protocolo de proceso o método."}, status=400)

            protocolo_obj = get_object_or_404(Protocolos, pk=protocolo_id) if protocolo_id else None
            protocolo_proceso_obj = get_object_or_404(Proceso, pk=protocolo_proceso_id) if protocolo_proceso_id else None
            metodo_obj = get_object_or_404(Metodo, pk=metodo_id) if metodo_id else None

            sistema_id = request.POST.get("sistema")
            if not sistema_id:
                return JsonResponse({"status": "error", "message": "Sistema no seleccionado"}, status=400)

            muestras_ids = request.POST.getlist("muestras")
            muestras_objs = []
            if (protocolo_proceso_obj or metodo_obj) and muestras_ids:
                muestras_objs = Muestras_y_Placebos.objects.filter(pk__in=muestras_ids)

            registrada_por = request.user
            fecha_registro = request.POST.get("fecha_registro")
            if not fecha_registro:
              fecha_registro = timezone.now()
            muestras_iterables = muestras_objs if muestras_objs else [None]
            observaciones = request.POST.get("observaciones")
            status = request.POST.get("status")
            invalidar_Secuencia = request.POST.get("invalidar_Secuencia")
            condicion = request.POST.get("condicion")
           # fecha_registro= request.POST.get("fecha_registro")
            fecha_invalidar = request.POST.get("fecha_invalidar")
            fecha_configuracion_protocolo_metodo = request.POST.get("fecha_configuracion_protocolo_metodo")
            fecha_configuracion_protocolo_proceso = request.POST.get("fecha_configuracion_protocolo_proceso")
            fecha_validar = request.POST.get("fecha_validar")
            fecha_impresion = request.POST.get("fecha_impresion")
            fecha_reporte = request.POST.get("fecha_reporte")
            fecha_auditada = request.POST.get("fecha_auditada")
            #registrada_por= request.POST.get("registrada_por")
            invalidar = request.POST.get("invalidar")
            validar = request.POST.get("validar")
            imprimir = request.POST.get("imprimir")
            reportar = request.POST.get("reportar")
            auditar = request.POST.get("auditar")
            parametros_ids = []
            if protocolo_obj:
                try:
                    parametros_raw = request.POST.get("parametros", "[]")
                    parametros_ids = json.loads(parametros_raw)
                    if not parametros_ids:
                        return JsonResponse({"status": "error", "message": "No se seleccionaron parámetros."}, status=400)
                except json.JSONDecodeError:
                    return JsonResponse({"status": "error", "message": "Error en el formato de parámetros."}, status=400)
            else:
                parametros_ids = [None]

            secuencias_creadas = []

            campos_comunes = {
                "nombre": nombre,
                "fecha_Inicio": fecha_inicio,
                "fecha_Final": fecha_Final,
                "protocolo": protocolo_obj,
                "protocolo_proceso": protocolo_proceso_obj,
                "metodo": metodo_obj,
                "sistema_id": sistema_id,
                "status": "Registrada",
                "invalidar_Secuencia": invalidar_Secuencia,
                "condicion": "Activo",
                "observaciones": observaciones,
                "parametro_sq": None,
                "fecha_registro": fecha_registro,
                "fecha_invalidar": fecha_invalidar,
                "fecha_configuracion_protocolo_metodo": fecha_configuracion_protocolo_metodo,
                "fecha_configuracion_protocolo_proceso": fecha_configuracion_protocolo_proceso,
                "fecha_validar": fecha_validar,
                "fecha_impresion": fecha_impresion,
                "fecha_reporte": fecha_reporte,
                "fecha_auditada": fecha_auditada,
                "registrada_por": registrada_por,
                "invalidar": invalidar,
                "validar": validar,
                "imprimir": imprimir,
                "reportar": reportar,
                "auditar": auditar,
            }

            for muestra in muestras_iterables:
                for parametro_id in parametros_ids:
                    parametro_obj = get_object_or_404(Parametro, pk=parametro_id) if parametro_id else None
                    campos_comunes["parametro_sq"] = parametro_obj
                    campos_comunes["muestras"] = muestra

                    try:
                        secuencia = Secuencias.objects.create(**campos_comunes)
                    except IntegrityError as e:
                        if 'unique' in str(e):
                            return JsonResponse({
                                "status": "error",
                                "message": "La(s) muestra(s) o parámetro(s) que seleccionaste ya están asociado(s) a éste protocolo"
                            }, status=400)
                        else:
                            raise 

                    muestras_relacionadas = []
                    if protocolo_obj:
                        muestras_relacionadas = protocolo_obj.muestras_y_Placebos.all()
                    elif protocolo_proceso_obj:
                        muestras_relacionadas = protocolo_proceso_obj.muestras.all()
                    elif metodo_obj and hasattr(metodo_obj, 'muestras_y_Placebos'):
                        muestras_relacionadas = metodo_obj.muestras_y_Placebos.all()

                    descripcion = [
                        [m.codigo_muestra_interno, m.lote_muestra, m.codigo_muestra_producto, str(m.etapa)]
                        for m in muestras_relacionadas
                    ]

                    muestra_data = {
                        "nombre": muestra.nombre_muestra,
                        "lote": muestra.lote_muestra,
                        "codigo_producto": muestra.codigo_muestra_producto,
                        "etapa": str(muestra.etapa)
                    } if muestra else None

                    secuencias_creadas.append({
                        "id": secuencia.id,
                        "nombre": secuencia.nombre,
                        "fecha_Inicio": secuencia.fecha_Inicio,
                        "protocolo": str(secuencia.protocolo) if secuencia.protocolo else None,
                        "protocolo_proceso": str(secuencia.protocolo_proceso) if secuencia.protocolo_proceso else None,
                        "metodo": str(secuencia.metodo) if secuencia.metodo else None,
                        "parametro": str(secuencia.parametro_sq) if parametro_obj else None,
                        "descripcion": descripcion,
                        "muestra_proceso": muestra_data,
                        "sistema": str(secuencia.sistema),
                    })

            return JsonResponse({
                "status": "ok",
                "message": f"{len(secuencias_creadas)} secuencia(s) creada(s) correctamente",
                "secuencias": secuencias_creadas
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Error al guardar: {str(e)}"
            }, status=400)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

#Select Encadenados segun protocolo de metodo o proceso
@login_required
def obtener_parametros_por_protocolo(request, protocolo_id):
    try:
        protocolo = Protocolos.objects.get(pk=protocolo_id)
        parametros = protocolo.parametro.all()  # asumiendo ManyToMany
        data = [{"id": p.id, "nombre": str(p)} for p in parametros]
        return JsonResponse({"parametros": data})
    except Protocolos.DoesNotExist:
        return JsonResponse({"parametros": []})
    
@login_required
def obtener_muestras_por_proceso(request, proceso_id):
    try:
        proceso = Proceso.objects.get(pk=proceso_id)
        muestras = proceso.muestras.all()  # ManyToMany
        data = [{"id": m.id, "nombre": str(m)} for m in muestras]
        return JsonResponse({"muestras": data})
    except Proceso.DoesNotExist:
        return JsonResponse({"muestras": []})

@login_required
def get_parametros_por_protocolo(request, protocolo_id):
   parametros = Parametro.objects.filter(protocolo_id=protocolo_id)
   parametros_data = [{'id': p.id, 'nombre': str(p)} for p in parametros]
   return JsonResponse({'parametros': parametros_data}) 

@login_required
def obtener_protocolos_proceso_activos(request):
    protocolos = Proceso.objects.filter(condicion='Activo', estado_del_proceso__id=1)
    data = [{"id": p.id, "nombre": str(p)} for p in protocolos]
    return JsonResponse({"protocolos": data})

@login_required
@require_http_methods(["GET", "POST"])
def editar_secuencias_protocolo_metodo(request, secuencia_id):
    from django.apps import apps
    secuencia = get_object_or_404(Secuencias, pk=secuencia_id)

    if request.method == "GET":
        data = {
            "id": secuencia.id,
            "nombre": secuencia.nombre,
            "fecha_Inicio": secuencia.fecha_Inicio.strftime("%Y-%m-%dT%H:%M") if secuencia.fecha_Inicio else '',
            "fecha_Final": secuencia.fecha_Final.strftime("%Y-%m-%dT%H:%M") if secuencia.fecha_Final else '',
            "protocolo": secuencia.protocolo.id if secuencia.protocolo else '',
            "protocolo_proceso": secuencia.protocolo_proceso.id if secuencia.protocolo_proceso else '',
            "metodo": secuencia.metodo.id if secuencia.metodo else '',
            "parametro_sq": secuencia.parametro_sq.id if secuencia.parametro_sq else '',
            "muestras": secuencia.muestras.id if secuencia.muestras else '',
            "status": secuencia.status,
            "invalidar_Secuencia": secuencia.invalidar_Secuencia,
            "condicion": secuencia.condicion,
            "observaciones": secuencia.observaciones,
            "sistema": secuencia.sistema.id if secuencia.sistema else '',
        }
        return JsonResponse(data)

    elif request.method == "POST":
        try:
            nombre = request.POST.get("nombre", "").strip()
            fecha_inicio_str = request.POST.get("fecha_Inicio", "").strip()
            protocolo_id = request.POST.get("protocolo")
            protocolo_proceso_id = request.POST.get("protocolo_proceso")
            metodo_id = request.POST.get("metodo")
            muestras_id = request.POST.get("muestras")
            observaciones = request.POST.get("observaciones", "").strip()
            sistema_id = request.POST.get("sistema")
            parametro_id = request.POST.get("parametro_sq")

            # Validar fecha
            fecha_inicio = parse_datetime(fecha_inicio_str) if fecha_inicio_str else None
            if fecha_inicio_str and fecha_inicio is None:
                return JsonResponse({"message": "Fecha de inicio inválida"}, status=400)

            # Obtener modelos dinámicamente 
            Sistema = apps.get_model('Secuencias', 'Sistema')
            ProtocoloProceso = apps.get_model('Protocolo_Muestras', 'Proceso')
            Muestras = apps.get_model('Protocolo_Metodos', 'Muestras_y_Placebos')
            Protocolo = apps.get_model('Protocolo_Metodos', 'Protocolos')
            Parametro = apps.get_model('Protocolo_Metodos', 'Parametro')
            Metodo = apps.get_model('Protocolo_Metodos', 'Metodo')

            # Asignaciones
            secuencia.nombre = nombre
            secuencia.fecha_Inicio = fecha_inicio
            secuencia.sistema = Sistema.objects.get(pk=sistema_id) if sistema_id else None
            secuencia.protocolo_proceso = ProtocoloProceso.objects.get(pk=protocolo_proceso_id) if protocolo_proceso_id else None
            secuencia.muestras = Muestras.objects.get(pk=muestras_id) if muestras_id else None
            secuencia.protocolo = Protocolo.objects.get(pk=protocolo_id) if protocolo_id else None
            secuencia.metodo = Metodo.objects.get(pk=metodo_id) if metodo_id else None
            secuencia.parametro_sq = Parametro.objects.get(pk=parametro_id) if parametro_id else None
            secuencia.observaciones = observaciones

            try:
                secuencia.save()
            except IntegrityError as e:
                if 'unique' in str(e):
                    return JsonResponse({
                        "status": "error",
                        "message": "La(s) muestra(s) o parámetro(s) que seleccionaste ya están asociado(s) a éste protocolo"
                    }, status=400)
                else:
                    raise  

            descripcion = []
            try:
                if secuencia.protocolo:
                    muestras = secuencia.protocolo.muestras_y_Placebos.all()
                elif secuencia.protocolo_proceso:
                    muestras = secuencia.protocolo_proceso.muestras.all()
                elif secuencia.metodo and hasattr(secuencia.metodo, 'muestras_y_Placebos'):
                    muestras = secuencia.metodo.muestras_y_Placebos.all()
                else:
                    muestras = []

                descripcion = [
                    [m.codigo_muestra_interno, m.lote_muestra, m.codigo_muestra_producto, str(m.etapa)]
                    for m in muestras
                ]
            except Exception as e:
                print(f"⚠️ Error al construir descripción: {e}")

            return JsonResponse({
                "message": "Secuencia actualizada correctamente",
                "secuencia": {
                    "id": secuencia.id,
                    "nombre": secuencia.nombre,
                    "protocolo": str(secuencia.protocolo) if secuencia.protocolo else None,
                    "protocolo_proceso": str(secuencia.protocolo_proceso) if secuencia.protocolo_proceso else None,
                    "metodo": str(secuencia.metodo) if secuencia.metodo else None,
                    "parametro": str(secuencia.parametro_sq) if secuencia.parametro_sq else None,
                    "descripcion": descripcion,
                    "muestra_proceso": {
                        "nombre": secuencia.muestras.nombre_muestra if secuencia.muestras else '',
                        "lote": secuencia.muestras.lote_muestra if secuencia.muestras else '',
                        "codigo_producto": secuencia.muestras.codigo_muestra_producto if secuencia.muestras else '',
                        "etapa": str(secuencia.muestras.etapa) if secuencia.muestras else '',
                    } if secuencia.protocolo_proceso or secuencia.metodo else None,
                    "sistema": str(secuencia.sistema) if secuencia.sistema else '',
                    "fecha_Inicio": secuencia.fecha_Inicio.strftime("%Y-%m-%dT%H:%M") if secuencia.fecha_Inicio else '',
                }
            })

        except Exception as e:
            return JsonResponse({
                "message": f"Error al actualizar secuencia: {str(e)}"
            }, status=400)
        
@login_required
def duplicar_secuencia_parametro(request, secuencia_id):
    print(f"📥 Recibido duplicado para secuencia: {secuencia_id}")
    
    if request.method != "POST":
        return JsonResponse({"message": "Método no permitido"}, status=405)

    try:
        secuencia = get_object_or_404(Secuencias, pk=secuencia_id)
        body = json.loads(request.body)
        parametros = body.get("parametros", [])

        if not parametros:
            return JsonResponse({"message": "Debe seleccionar al menos un parámetro"}, status=400)

        from django.apps import apps
        Parametro = apps.get_model('Protocolo_Metodos', 'Parametro')

        nuevas_secuencias = []

        for param_id in parametros:
            parametro_obj = Parametro.objects.get(pk=param_id)

            try:
                nueva = Secuencias.objects.create(
                    nombre=f"{secuencia.nombre} ",
                    fecha_Inicio=secuencia.fecha_Inicio,
                    protocolo=secuencia.protocolo,
                    protocolo_proceso=secuencia.protocolo_proceso,
                    metodo=secuencia.metodo,
                    muestras=secuencia.muestras,
                    sistema=secuencia.sistema,
                    observaciones=secuencia.observaciones,
                    parametro_sq=parametro_obj,
                    fecha_configuracion_protocolo_metodo="0001-01-01",
                    fecha_configuracion_protocolo_proceso=now()
                )
            except IntegrityError as e:
                if 'unique' in str(e):
                    return JsonResponse({
                        "status": "error",
                        "message": "La(s) muestra(s) o parámetro(s) que seleccionaste ya están asociado(s) a éste protocolo"
                    }, status=400)
                else:
                    raise

            muestras = []
            if nueva.protocolo:
                muestras = nueva.protocolo.muestras_y_Placebos.all()
            elif nueva.protocolo_proceso:
                muestras = nueva.protocolo_proceso.muestras.all()
            elif nueva.metodo and hasattr(nueva.metodo, 'muestras_y_Placebos'):
                muestras = nueva.metodo.muestras_y_Placebos.all()

            descripcion = [
                [m.codigo_muestra_interno, m.lote_muestra, m.codigo_muestra_producto, str(m.etapa)]
                for m in muestras
            ]

            nuevas_secuencias.append({
                "id": nueva.id,
                "nombre": nueva.nombre,
                "fecha_inicio": nueva.fecha_Inicio,
                "protocolo": str(nueva.protocolo) if nueva.protocolo else None,
                "protocolo_proceso": str(nueva.protocolo_proceso) if nueva.protocolo_proceso else None,
                "metodo": str(nueva.metodo) if nueva.metodo else None,
                "parametro": str(nueva.parametro_sq),
                "descripcion": descripcion,
                "muestra_proceso": {
                    "nombre": nueva.muestras.nombre_muestra if nueva.muestras else '',
                    "lote": nueva.muestras.lote_muestra if nueva.muestras else '',
                    "codigo_producto": nueva.muestras.codigo_muestra_producto if nueva.muestras else '',
                    "etapa": str(nueva.muestras.etapa) if nueva.muestras else '',
                } if nueva.protocolo_proceso or nueva.metodo else None,
                "sistema": str(nueva.sistema) if nueva.sistema else '',
            })

        return JsonResponse({
            "message": f"{len(nuevas_secuencias)} parámetro(s) agregado(s) correctamente.",
            "secuencias": nuevas_secuencias
        })

    except Exception as e:
        return JsonResponse({"message": f"Error al duplicar: {str(e)}"}, status=400)

@login_required
def duplicar_secuencia_muestras(request, secuencia_id):
    if request.method != "POST":
        return JsonResponse({"message": "Método no permitido"}, status=405)

    try:
        secuencia = get_object_or_404(Secuencias, pk=secuencia_id)
        body = json.loads(request.body)
        muestras_ids = body.get("muestras", [])

        if not muestras_ids:
            return JsonResponse({"message": "Debe seleccionar al menos una muestra"}, status=400)

        nuevas_secuencias = []

        for muestra_id in muestras_ids:
            muestra_obj = Muestras_y_Placebos.objects.get(pk=muestra_id)

            try:
                nueva = Secuencias.objects.create(
                    nombre=f"{secuencia.nombre} ",
                    fecha_Inicio=secuencia.fecha_Inicio,
                    protocolo=secuencia.protocolo,
                    protocolo_proceso=secuencia.protocolo_proceso,
                    metodo=secuencia.metodo,
                    muestras=muestra_obj,
                    sistema=secuencia.sistema,
                    observaciones=secuencia.observaciones,
                    parametro_sq=secuencia.parametro_sq,
                    fecha_configuracion_protocolo_metodo=now(),
                    fecha_configuracion_protocolo_proceso="0001-01-01"
                )
            except IntegrityError as e:
                if 'unique' in str(e).lower():
                    return JsonResponse({
                        "status": "error",
                        "message": "La(s) muestra(s) o parámetro(s) que seleccionaste ya están asociado(s) a éste protocolo"
                    }, status=400)
                else:
                    raise

            # Obtener muestras relacionadas para construir descripción
            muestras_relacionadas = []
            if nueva.protocolo:
                muestras_relacionadas = nueva.protocolo.muestras_y_Placebos.all()
            elif nueva.protocolo_proceso:
                muestras_relacionadas = nueva.protocolo_proceso.muestras.all()
            elif nueva.metodo and hasattr(nueva.metodo, 'muestras_y_Placebos'):
                muestras_relacionadas = nueva.metodo.muestras_y_Placebos.all()

            descripcion = [
                [m.codigo_muestra_interno, m.lote_muestra, m.codigo_muestra_producto, str(m.etapa)]
                for m in muestras_relacionadas
            ]

            muestra_data = {
                "nombre": muestra_obj.nombre_muestra,
                "lote": muestra_obj.lote_muestra,
                "codigo_producto": muestra_obj.codigo_muestra_producto,
                "etapa": str(muestra_obj.etapa)
            }

            nuevas_secuencias.append({
                "id": nueva.id,
                "nombre": nueva.nombre,
                "fecha_inicio": nueva.fecha_Inicio,
                "protocolo": str(nueva.protocolo) if nueva.protocolo else None,
                "protocolo_proceso": str(nueva.protocolo_proceso) if nueva.protocolo_proceso else None,
                "metodo": str(nueva.metodo) if nueva.metodo else None,
                "parametro": str(nueva.parametro_sq) if nueva.parametro_sq else None,
                "descripcion": descripcion,
                "muestra_proceso": muestra_data,
                "sistema": str(nueva.sistema),
            })

        return JsonResponse({
            "message": f"{len(nuevas_secuencias)} muestra(s) agregada(s) correctamente.",
            "secuencias": nuevas_secuencias
        })

    except Exception as e:
        return JsonResponse({"message": f"Error al duplicar muestras: {str(e)}"}, status=400)

