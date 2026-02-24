from django.shortcuts import render, get_object_or_404,  redirect
from .models import Proceso
from Aplicaciones.Secuencias.models import Secuencias
from .forms import ProcesoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse,HttpResponseBadRequest


@login_required
def protocolo_proceso(request):
    titulo = "Protocolo de Métodos"
    protocolo_proceso = Proceso.objects.all()
    is_admin = request.user.groups.filter(name='Administrador').exists()

    context = {
        "titulo": titulo,
        "protocolo_proceso": protocolo_proceso,
        "is_admin": is_admin, 
    }
    return render(request, "protocolo_proceso/protocolo_proceso.html", context)

@login_required
def protocolo_proceso_json(request):
    procesos = Proceso.objects.all()
    data = []
    for p in procesos:
        if p.condicion == "Activo" and p.estado_del_proceso and p.estado_del_proceso.id != 7:
            data.append({
                "id": p.id,
                "codigo": p.codigo,
                "nombre": p.nombre,
                "cliente": str(p.cliente),
                "observaciones": p.observaciones,
                "celda": {
                   "id": p.celda.id if p.celda else None,
                   "nombre": p.celda.nombre_celda if p.celda else "",
                   "responsable": p.celda.responsable.get_full_name() if p.celda and p.celda.responsable else ""
                  },
                "metodo": {
                   "id": p.metodo.id if p.metodo else None,
                   "código": p.metodo.codigo_metodo if p.metodo else "",
                    "nombre": p.metodo.nombre_metodo if p.metodo and p.metodo.nombre_metodo else ""
                    },
                "fecha_final": p.fecha_final.strftime('%Y-%m-%d') if p.fecha_final else '',
                "fecha_de_entrega": p.fecha_de_entrega.strftime('%Y-%m-%d') if p.fecha_de_entrega else '',
                "estado_del_proceso": {
                    "id": p.estado_del_proceso.id,
                    "nombre": str(p.estado_del_proceso)
                },
                "entregado_a": p.entregado_a
            })

    return JsonResponse(data, safe=False)

@login_required
def crear_protocolo_proceso(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ProcesoForm(request.POST)
        if form.is_valid():
            protocolo = form.save()
            return JsonResponse({"success": True, "message": "Protocolo creado satisfactoriamente"})
        else:
            return JsonResponse({
                "success": False,
                "errors": form.errors.as_json()
            }, status=400)
    elif request.method == "POST":
       
        return HttpResponseBadRequest("Bad request")
    else:
        form = ProcesoForm()
        return render(request, "protocolo_proceso/crear_protocolo_proceso.html", {
            "form": form,
            "titulo": "Crear Protocolos"
        })

@login_required
def editar_protocolo_proceso(request, pk):
    protocolo = get_object_or_404(Proceso, pk=pk)

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ProcesoForm(request.POST, instance=protocolo)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Protocolo actualizado correctamente"})
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()}, status=400)

    elif request.method == "POST":
        return HttpResponseBadRequest("Bad request")

    else:
        form = ProcesoForm(instance=protocolo)
        return render(request, "protocolo_proceso/edicion_protocolo_proceso.html", {
            "form": form,
            "protocolo": protocolo,
            "titulo": "Editar Protocolo Proceso"
        })

@login_required
def revisar_protocolo_proceso(request, pk):
    return render(request, 'protocolo_proceso/revisar_protocolo_proceso.html', {'protocolo_id': pk})

@login_required
def api_revisar_protocolo_proceso(request, pk):
    protocolo = Proceso.objects.get(id=pk)
    secuencias = Secuencias.objects.filter(protocolo_proceso=pk)
    muestras = protocolo.muestras.all()
    contar_muestras = muestras.count() or 1

    # Progreso por estado
    porcentaje_estado = {
        "Invalida": 0,
        "Ensayo": 0,
        "Registrada": 12.5,
        "Revisada": 25,
        "Impresa": 50,
        "Reportada": 75,
        "Auditada": 100,
    }

    # Priorización de estados (de mayor a menor)
    prioridad = ["Auditada", "Reportada", "Impresa", "Revisada", "Registrada", "Invalida", "Ensayo"]

    data = {
        "codigo": protocolo.codigo,
        "nombre": protocolo.nombre,
        "estado_protocolo": protocolo.estado_del_proceso.estado_protocolos if protocolo.estado_del_proceso else "",
        "observaciones": protocolo.observaciones or "",
        "muestras": [],
    }

    for muestra in muestras:
        # Todas las secuencias asociadas a esta muestra
        secuencias_muestra = secuencias.filter(muestras=muestra)
        estados = [s.status for s in secuencias_muestra if s.status]

        # Encontrar el estado con mayor prioridad
        estado_prioritario = None
        for estado in prioridad:
            if estado in estados:
                estado_prioritario = estado
                break

        progreso = porcentaje_estado.get(estado_prioritario, 0)

        etapa = muestra.etapa
        nombre_etapa = etapa.nombre_etapa if etapa else ''
        nombre_ensayo = etapa.ensayo.nombre_ensayo if etapa and etapa.ensayo else ''

        data["muestras"].append({
            "etapa": f"{nombre_etapa} {nombre_ensayo}",
            "lote_muestra": muestra.lote_muestra,
            "codigo_muestra_producto": muestra.codigo_muestra_producto,
            "estado": estado_prioritario or "Sin estado",
            "progreso": progreso
        })

    # Parámetros
    data["parametros"] = [
        {
            "nombre": f"{muestra['etapa']} (Lote: {muestra['lote_muestra']})",
            "estado": muestra["estado"]
        }
        for muestra in data["muestras"]
    ]

    # Porcentajes globales (igual que antes)
    def porcentaje(status, valor):
        count = secuencias.filter(status=status).count()
        return count * valor / contar_muestras

    data["porcentajes"] = {
        "Registrada": porcentaje("Registrada", 12.5),
        "Revisada": porcentaje("Revisada", 25),
        "Impresa": porcentaje("Impresa", 50),
        "Reportada": porcentaje("Reportada", 75),
        "Auditada": porcentaje("Auditada", 100)
    }

    return JsonResponse(data)

