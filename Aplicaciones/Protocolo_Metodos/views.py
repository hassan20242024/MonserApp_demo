from django.shortcuts import render, redirect, get_object_or_404
from .models import Protocolos,Subparametro, Parametro, Metodologia,EstadoProtocolo,Viabilidad,Titulo_Parametro,Celda,Muestras_y_Placebos,Ensayo, Cliente, Celda, Metodo, Tipo_muestra, Etapa
from Aplicaciones.Protocolo_Muestras.models import ViabilidadProceso
from django.contrib.auth.models import User
from .forms import ProtocolosForm,ParametroForm, MetodologiaForm, EstadoProtocoloForm, crear_ensayoForm,ViabilidadForm,sistemaForm, SubparametroForm,Titulo_ParametroForm, ingresar_muestrasForm, clienteForm, CeldaForm, MetodoForm, tipo_muestrasForm, EtapaForm, viavilidad_procesoForm
from Aplicaciones.Secuencias.models import Secuencias, Sistema
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
from django.template.loader import render_to_string
import traceback


def group_required(group_name):
    return user_passes_test(
        lambda user: user.is_authenticated and (
            user.is_superuser or user.groups.filter(name=group_name).exists()
        )
    )
@login_required
def protocolo_metodos(request):
    is_admin = request.user.groups.filter(name='Administrador').exists()
    context = {
        "is_admin": is_admin,
    }
    return render(request, "protocolo_metodos/protocolo_metodos.html", context)

@login_required
def protocolo_metodos_json(request):
    protocolos = Protocolos.objects.filter(condicion="Activo").exclude(estado_protocolo__id=7)
    data = []
    for p in protocolos:
        estado = p.estado_protocolo
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
            "estado_protocolo": {
                "id": estado.id if estado else None,
                "nombre": str(estado) if estado else '',
            },
             "entregado_a": p.entregado_a,
        })
    return JsonResponse(data, safe=False)

@login_required
def crear_protocolo_metodos(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ProtocolosForm(request.POST)
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
        form = ProtocolosForm()
        return render(request, "protocolo_metodos/crear_protocolo_metodos.html", {
            "form": form,
            "titulo": "Crear Protocolos"
        })

@login_required
@group_required('Administrador')
def configuracion_protocolo_metodos(request):
    titulo = "Ajustes Protocolo de Métodos/Parámetros"
    Pto=Parametro.objects.all()
    tituloParametro=Titulo_Parametro.objects.all()
    nombreSubparametro=Subparametro.objects.all()

    if request.method == "POST":
        form = ParametroForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("configuracion_protocolo_metodos")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = ParametroForm() 
    
    context={
        "titulo":titulo,
        "form":form,
       "Pto": Pto,
       "tituloParametro":tituloParametro,
       "nombreSubparametro":nombreSubparametro
    }
   
    return render(request, "protocolo_metodos/configuracion_protocolo_metodos.html", context)

@login_required
def editar_protocolo_metodos(request, pk):
    protocolo = get_object_or_404(Protocolos, pk=pk)

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ProtocolosForm(request.POST, instance=protocolo)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Protocolo actualizado correctamente"})
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()}, status=400)

    elif request.method == "POST":
        return HttpResponseBadRequest("Bad request")

    else:
        form = ProtocolosForm(instance=protocolo)
        return render(request, "protocolo_metodos/edicion_protocolo_metodos.html", {
            "form": form,
            "protocolo": protocolo,
            "titulo": "Editar Protocolo"
        })

@login_required
def revisar_protocolo_metodos(request, pk):
    return render(request, 'protocolo_metodos/revisar_protocolo_metodos.html', {'protocolo_id': pk})

@login_required
def api_revisar_protocolo_metodos(request, pk):
    protocolo = Protocolos.objects.get(id=pk)
    secuencias = Secuencias.objects.filter(protocolo=pk)
    parametros = protocolo.parametro.all()
    contar_parametros = parametros.count()
    # Mapeo de progreso por estado
    porcentaje_estado = {
        "Invalida": 0,
        "Ensayo": 0,
        "Registrada": 12.5,
        "Revisada": 25,
        "Impresa": 50,
        "Reportada": 75,
        "Auditada": 100,
    }
    # Priorización del estado más alto
    prioridad = ["Auditada", "Reportada", "Impresa", "Revisada", "Registrada", "Invalida", "Ensayo"]

    data = {
        "codigo": protocolo.codigo,
        "nombre": protocolo.nombre,
        "estado_protocolo": protocolo.estado_protocolo.estado_protocolos if protocolo.estado_protocolo else "",
        "observaciones": protocolo.observaciones or "",
        "parametros": []
    }

    for parametro in parametros:
        # Filtramos todas las secuencias que usan este parámetro
        secuencias_parametro = secuencias.filter(parametro_sq=parametro)
        estados = [s.status for s in secuencias_parametro if s.status]

        # Determinar el estado prioritario
        estado_prioritario = None
        for estado in prioridad:
            if estado in estados:
                estado_prioritario = estado
                break

        progreso = porcentaje_estado.get(estado_prioritario, 0)

        data["parametros"].append({
            "nombre": str(parametro),  # Usa el __str__ del modelo Parametro
            "estado": estado_prioritario or "Sin estado",
            "progreso": progreso
        })

    # Porcentajes globales acumulados
    def porcentaje(status, valor):
        count = secuencias.filter(status=status).count()
        return count * valor / contar_parametros if contar_parametros > 0 else 0

    data["porcentajes"] = {
        "Registrada": porcentaje("Registrada", 12.5),
        "Revisada": porcentaje("Revisada", 25),
        "Impresa": porcentaje("Impresa", 50),
        "Reportada": porcentaje("Reportada", 75),
        "Auditada": porcentaje("Auditada", 100)
    }

    return JsonResponse(data)

@login_required
@group_required('Administrador')
def editar_parametro(request, pk):
    titulo="Editar Parámetros"
   
    if request.method == "POST":
        Pto=Parametro.objects.get(pk=pk)
        form = ParametroForm(request.POST, instance=Pto)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("configuracion_protocolo_metodos")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = ParametroForm(instance=Pto)

    context={
        "titulo":titulo,
        "form":form,
        "Pto":Pto
    }
    return render(request, "protocolo_metodos/configuracion_protocolo_metodos.html", context)

@login_required
@group_required('Administrador')
def subparametro(request):
    titulo="Ajustes Protocolo de Métodos/Subparametros"
    subparametro=Subparametro.objects.all()
    
    if request.method == "POST":
        form = SubparametroForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("subparametro")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = SubparametroForm() 
    context={
        "titulo":titulo,
        "form":form,
        "subparametro":subparametro
    }
    return render(request, "protocolo_metodos/subparametro.html", context)

@login_required
@group_required('Administrador')
def editar_subparametro(request, pk):
    titulo = "Ajustes Protocolo de Métodos/Subparametros"
    subparametro_obj = Subparametro.objects.get(id=pk)
    
    if request.method == "POST":
        form = SubparametroForm(request.POST, instance=subparametro_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("subparametro")
        else:
            messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = SubparametroForm(instance=subparametro_obj)

    # PASAMOS TODOS LOS SUBPARAMETROS PARA ITERAR EN LA TABLA
    subparametro = Subparametro.objects.all()

    context = {
        "titulo": titulo,
        "form": form,
        "subparametro": subparametro
    }
    return render(request, "protocolo_metodos/subparametro.html", context)
@login_required
@group_required('Administrador')
def titulo_parametro(request):
    titulo="Ajustes Protocolo de Métodos/Titulo parámetro"
    titulo_parametro=Titulo_Parametro.objects.all()
    
    if request.method == "POST":
        form = Titulo_ParametroForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("titulo_parametro")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = Titulo_ParametroForm() 
    context={
        "titulo":titulo,
        "form":form,
        "titulo_parametro":titulo_parametro
    }
    return render(request, "protocolo_metodos/titulo_parametro.html", context)

@login_required
@group_required('Administrador')
def editar_titulo_parametro(request, pk):
    titulo="Editar Título Parámetro"
    titulo_parametro=Titulo_Parametro.objects.get(id=pk)
   
    if request.method == "POST":
        form = Titulo_ParametroForm(request.POST, instance=titulo_parametro)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("titulo_parametro")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = Titulo_ParametroForm(instance=titulo_parametro)

    context={
        "titulo":titulo,
        "form":form,
        "titulo_parametro":titulo_parametro
    }
    return render(request, "protocolo_metodos/titulo_parametro.html", context)

@login_required
@group_required('Administrador')
def crear_metodologia(request):
    titulo="Ajustes Protocolo de Métodos/Metodologia"
    crear_metodologia=Metodologia.objects.all()
    
    
    if request.method == "POST":
        form = MetodologiaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("crear_metodologia")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = MetodologiaForm() 
    context={
        "titulo":titulo,
        "form":form,
        "crear_metodologia":crear_metodologia
    }
    return render(request, "protocolo_metodos/crear_metodologia.html", context)

@login_required
@group_required('Administrador')
def editar_metodologia(request, pk):
    titulo = "Ajustes Protocolo de Métodos/Metodologia"
    crear_metodologia_obj = Metodologia.objects.get(id=pk)
    
    if request.method == "POST":
        form = MetodologiaForm(request.POST, instance=crear_metodologia_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("crear_metodologia")
        else:
            messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = MetodologiaForm(instance=crear_metodologia_obj)

    # PASAMOS TODOS LOS REGISTROS PARA EL FOR
    crear_metodologia = Metodologia.objects.all()

    context = {
        "titulo": titulo,
        "form": form,
        "crear_metodologia": crear_metodologia
    }
    return render(request, "protocolo_metodos/crear_metodologia.html", context)
@login_required
@group_required('Administrador')
def definir_estado(request):
    titulo="Ajustes Protocolo de Métodos/Estado"
    definir_estado=EstadoProtocolo.objects.all()
    
    
    if request.method == "POST":
        form = EstadoProtocoloForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("definir_estado")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = EstadoProtocoloForm() 
    context={
        "titulo":titulo,
        "form":form,
        "definir_estado":definir_estado
    }
    return render(request, "protocolo_metodos/definir_estado.html", context)

@login_required
@group_required('Administrador')
def editar_definir_estado(request, pk):
    titulo = "Ajustes Protocolo de Métodos/Estado"
    estado_obj = EstadoProtocolo.objects.get(id=pk)
    
    if request.method == "POST":
        form = EstadoProtocoloForm(request.POST, instance=estado_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("definir_estado")
        else:
            messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = EstadoProtocoloForm(instance=estado_obj)

    # PASAMOS TODOS LOS ESTADOS PARA ITERAR EN LA TABLA
    definir_estado = EstadoProtocolo.objects.all()

    context = {
        "titulo": titulo,
        "form": form,
        "definir_estado": definir_estado
    }
    return render(request, "protocolo_metodos/definir_estado.html", context)
@login_required
@group_required('Administrador')
def crear_ensayo(request):
    titulo="Ajustes Protocolo de Métodos/Ensayo"
    crear_ensayo=Ensayo.objects.all()
    if request.method == "POST":
        form = crear_ensayoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("crear_ensayo")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = crear_ensayoForm() 
    context={
        "titulo":titulo,
        "form":form,
        "crear_ensayo":crear_ensayo,
        
    }
    return render(request, "protocolo_metodos/crear_ensayo.html", context)

@login_required
@group_required('Administrador')
def editar_ensayo(request, pk):
    titulo = "Ajustes Protocolo de Métodos/Ensayo"
    ensayo_obj = Ensayo.objects.get(id=pk)
    
    if request.method == "POST":
        form = crear_ensayoForm(request.POST, instance=ensayo_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("crear_ensayo")
        else:
            messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = crear_ensayoForm(instance=ensayo_obj)

    # PASAMOS TODOS LOS ENSAYOS PARA ITERAR EN LA TABLA
    crear_ensayo = Ensayo.objects.all()

    context = {
        "titulo": titulo,
        "form": form,
        "crear_ensayo": crear_ensayo
    }
    return render(request, "protocolo_metodos/crear_ensayo.html", context)
@login_required
@group_required('Administrador')
def insumosDelProceso(request):
    titulo="Ajustes Protocolo de Métodos/Insumos del Proceso"
    viabilidad=Viabilidad.objects.all()
    
    
    if request.method == "POST":
        form = ViabilidadForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("insumosDelProceso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = ViabilidadForm() 
    context={
        "titulo":titulo,
        "form":form,
        "viabilidad":viabilidad
    }
    return render(request, "protocolo_metodos/insumosDelProceso.html", context)

@login_required
@group_required('Administrador')
def editar_insumosDelProceso(request, pk):
    titulo = "Ajustes Protocolo de Métodos/Insumos del Proceso"
    viabilidad_obj = Viabilidad.objects.get(id=pk)
    
    if request.method == "POST":
        form = ViabilidadForm(request.POST, instance=viabilidad_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("insumosDelProceso")
        else:
            messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = ViabilidadForm(instance=viabilidad_obj)

    # PASAMOS TODOS LOS REGISTROS PARA ITERAR EN LA TABLA
    viabilidad = Viabilidad.objects.all()

    context = {
        "titulo": titulo,
        "form": form,
        "viabilidad": viabilidad
    }
    return render(request, "protocolo_metodos/insumosDelProceso.html", context)
@login_required
@group_required('Administrador')
def crear_cliente(request):
    titulo="Ajustes Protocolo de Métodos/Clientes"
    crear_cliente=Cliente.objects.all()
    if request.method == "POST":
        form = clienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("crear_cliente")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = clienteForm() 
    context={
        "titulo":titulo,
        "form":form,
        "crear_cliente":crear_cliente,
        
    }
    return render(request, "protocolo_metodos/clientes.html", context)
    
@login_required
@group_required('Administrador')
def editar_cliente(request, pk):
    titulo = "Ajustes Protocolo de Métodos/Clientes"
    cliente_obj = Cliente.objects.get(id=pk)
    
    if request.method == "POST":
        form = clienteForm(request.POST, instance=cliente_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("crear_cliente")
        else:
            messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = clienteForm(instance=cliente_obj)

    # PASAMOS TODOS LOS CLIENTES PARA ITERAR EN LA TABLA
    crear_cliente = Cliente.objects.all()

    context = {
        "titulo": titulo,
        "form": form,
        "crear_cliente": crear_cliente
    }
    return render(request, "protocolo_metodos/clientes.html", context)
@login_required
def detalles_protocolo_metodos(request):
    titulo = "Detalles del Protocolo"
    protocolo_metodos=Protocolos.objects.all()
    context = {

        "titulo": titulo,
        "protocolo_metodos": protocolo_metodos,
    }
    return render(request, "protocolo_metodos/detalles_protocolo_metodos.html", context)

@login_required
def muestras(request):
    titulo = "Muestras de Análisis"
    context = {
        "titulo": titulo,
    }
    return render(request, "protocolo_metodos/muestras.html", context)

@login_required
def muestras_json(request):
    muestras = Muestras_y_Placebos.objects.filter(condicion="Activo")
    data = []

    for m in muestras:
        data.append({
            "fecha_ingreso": m.fecha_ingreso.strftime("%Y-%m-%d"),
            "nombre_muestra": m.nombre_muestra,
            "lote_muestra": m.lote_muestra,
            "tipo_muestra": str(m.tipo_muestra),
            "etapa": str(m.etapa),
            "codigo_muestra_interno": m.codigo_muestra_interno,
            "codigo_muestra_producto": m.codigo_muestra_producto,
            "observaciones_muestras": m.observaciones_muestras,
            "pk": m.pk,
        })

    return JsonResponse({"data": data})

@login_required
def lista_etapas(request):
    if request.method == "GET":
        etapas = Etapa.objects.select_related('ensayo').all()
        data = [
            {
                "id": etapa.id,
                "etapa": f"{etapa.nombre_etapa} {etapa.ensayo.nombre_ensayo}"
            }
            for etapa in etapas
        ]
        return JsonResponse(data, safe=False)
    
@login_required
def ingresar_muestras(request):
    if request.method == "GET":
        form = ingresar_muestrasForm()
        html = render_to_string(
            "protocolo_metodos/partial_muestra_form.html", { "form": form,
                "editar": False,      
                "etapa_actual_id": ""}, request=request
        )
        return JsonResponse({"html_form": html})

    form = ingresar_muestrasForm(request.POST)
    etapas_ids = request.POST.getlist("etapa") or []

    if not form.is_valid():
        html = render_to_string(
            "protocolo_metodos/partial_muestra_form.html", {"form": form}, request=request
        )
        return JsonResponse({
            "success": False,
            "html_form": html,
            "message": "Error al validar formulario"
        }, status=400)

    cd = form.cleaned_data
    duplicados = []

    for etapa_id in etapas_ids:
        try:
            etapa = Etapa.objects.get(pk=etapa_id)
        except Etapa.DoesNotExist:
            continue

        if Muestras_y_Placebos.objects.filter(
            lote_muestra=cd['lote_muestra'], etapa=etapa
        ).exists():
            duplicados.append(
                f"El lote <strong>{cd['lote_muestra']}</strong> ya está asociado a la etapa <strong>{etapa}</strong>."
            )

    if duplicados:
        return JsonResponse({
            "success": False,
            "duplicados": duplicados,
            "message": "No se guardó por duplicados."
        }, status=400)

    try:
        total_guardados = 0
        muestras_guardadas = []

        for etapa_id in etapas_ids:
            etapa = Etapa.objects.get(pk=etapa_id)
            nueva_muestra = Muestras_y_Placebos.objects.create(
                nombre_muestra=cd['nombre_muestra'],
                fecha_ingreso=cd['fecha_ingreso'],
                lote_muestra=cd['lote_muestra'],
                tipo_muestra=cd['tipo_muestra'],
                etapa=etapa,
                codigo_muestra_interno=cd['codigo_muestra_interno'],
                codigo_muestra_producto=cd['codigo_muestra_producto'],
                observaciones_muestras=cd['observaciones_muestras'],
            )
            total_guardados += 1

            muestras_guardadas.append({
                "pk": nueva_muestra.pk,
                "fecha_ingreso": nueva_muestra.fecha_ingreso.strftime("%Y-%m-%d"),
                "nombre_muestra": str(nueva_muestra.nombre_muestra),
                "lote_muestra": str(nueva_muestra.lote_muestra),
                "tipo_muestra": str( nueva_muestra.tipo_muestra),
                "etapa": str(nueva_muestra.etapa),
                "codigo_muestra_interno": nueva_muestra.codigo_muestra_interno,
                "codigo_muestra_producto": nueva_muestra.codigo_muestra_producto,
                "observaciones_muestras": nueva_muestra.observaciones_muestras,
            })

        return JsonResponse({
            "success": True,
            "message": f"{total_guardados} muestra(s) guardada(s) correctamente.",
            "muestras": muestras_guardadas
        })

    except IntegrityError:
        return JsonResponse({
            "success": False,
            "message": "Error de integridad: posible duplicado."
        }, status=400)

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Error inesperado en el servidor.",
           "traceback": str(traceback.format_exc())
        }, status=500)

@login_required
def editar_muestras(request, pk):
    muestra = get_object_or_404(Muestras_y_Placebos, pk=pk)

    if request.method == "GET":
        form = ingresar_muestrasForm(instance=muestra)
        html = render_to_string("protocolo_metodos/partial_muestra_form.html", {
            "form": form,
            "editar": True,
            "muestra": muestra,
            "etapa_actual_id": muestra.etapa.id if muestra.etapa else None  
        }, request=request)
        return JsonResponse({"html_form": html})

    form = ingresar_muestrasForm(request.POST, instance=muestra)
    etapas_ids = request.POST.getlist("etapa") or []

    if not form.is_valid():
        html = render_to_string("protocolo_metodos/partial_muestra_form.html", {
            "form": form,
            "editar": True,
            "muestra": muestra
        }, request=request)
        return JsonResponse({
            "success": False,
            "html_form": html,
            "message": "Error al validar formulario"
        }, status=400)

    # VALIDAR DUPLICADOS
    cd = form.cleaned_data
    duplicados = []

    for etapa_id in etapas_ids:
        try:
            etapa = Etapa.objects.get(pk=etapa_id)
        except Etapa.DoesNotExist:
            continue

        if Muestras_y_Placebos.objects.filter(
            lote_muestra=cd['lote_muestra'],
            etapa=etapa
        ).exclude(pk=muestra.pk).exists():  # 👈 Excluye la muestra actual
            duplicados.append(
                f"El lote <strong>{cd['lote_muestra']}</strong> ya está asociado a la etapa <strong>{etapa}</strong>."
            )

    if duplicados:
        return JsonResponse({
            "success": False,
            "duplicados": duplicados,
            "message": "No se guardó por duplicados."
        }, status=400)

    # GUARDAR
    try:
        muestra = form.save(commit=False)
        muestra.etapa = Etapa.objects.get(pk=etapas_ids[0]) if etapas_ids else None
        muestra.save()

        return JsonResponse({
            "success": True,
            "message": "Muestra actualizada correctamente."
        })

    except IntegrityError:
        return JsonResponse({
            "success": False,
            "message": "Error de integridad: posible duplicado."
        }, status=400)

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Error inesperado en el servidor.",
            "traceback": str(traceback.format_exc())
        }, status=500)


@login_required
def duplicar_muestras(request, pk):
    original = get_object_or_404(Muestras_y_Placebos, pk=pk)

    if request.method == "GET":
        # Prellenar el formulario con los datos de la muestra original
        initial_data = {
            'nombre_muestra': original.nombre_muestra,
            'fecha_ingreso': original.fecha_ingreso,
            'lote_muestra': original.lote_muestra,
            'tipo_muestra': original.tipo_muestra,
            'codigo_muestra_interno': original.codigo_muestra_interno,
            'codigo_muestra_producto': original.codigo_muestra_producto,
            'observaciones_muestras': original.observaciones_muestras,
        }

        form = ingresar_muestrasForm(initial=initial_data)
        html = render_to_string("protocolo_metodos/partial_muestra_form.html", {
            "form": form,
            "duplicar": True,
            "editar": False,
            "etapa_actual_id": original.etapa.id if original.etapa else ""
        }, request=request)

        return JsonResponse({"html_form": html})

    # POST: Validar y guardar como nueva muestra
    form = ingresar_muestrasForm(request.POST)
    etapas_ids = request.POST.getlist("etapa") or []

    if not form.is_valid():
        html = render_to_string("protocolo_metodos/partial_muestra_form.html", {
            "form": form,
            "duplicar": True
        }, request=request)
        return JsonResponse({
            "success": False,
            "html_form": html,
            "message": "Error al validar formulario"
        }, status=400)

    cd = form.cleaned_data
    duplicados = []

    for etapa_id in etapas_ids:
        try:
            etapa = Etapa.objects.get(pk=etapa_id)
        except Etapa.DoesNotExist:
            continue

        if Muestras_y_Placebos.objects.filter(
            lote_muestra=cd['lote_muestra'], etapa=etapa
        ).exists():
            duplicados.append(
                f"El lote <strong>{cd['lote_muestra']}</strong> ya está asociado a la etapa <strong>{etapa}</strong>."
            )

    if duplicados:
        return JsonResponse({
            "success": False,
            "duplicados": duplicados,
            "message": "No se guardó por duplicados."
        }, status=400)

    try:
        total_guardados = 0
        muestras_guardadas = []

        for etapa_id in etapas_ids:
            etapa = Etapa.objects.get(pk=etapa_id)
            nueva_muestra = Muestras_y_Placebos.objects.create(
                nombre_muestra=cd['nombre_muestra'],
                fecha_ingreso=cd['fecha_ingreso'],
                lote_muestra=cd['lote_muestra'],
                tipo_muestra=cd['tipo_muestra'],
                etapa=etapa,
                codigo_muestra_interno=cd['codigo_muestra_interno'],
                codigo_muestra_producto=cd['codigo_muestra_producto'],
                observaciones_muestras=cd['observaciones_muestras'],
            )
            total_guardados += 1

            muestras_guardadas.append({
                "pk": nueva_muestra.pk,
                "fecha_ingreso": nueva_muestra.fecha_ingreso.strftime("%Y-%m-%d"),
                "nombre_muestra": str(nueva_muestra.nombre_muestra),
                "lote_muestra": str(nueva_muestra.lote_muestra),
                "tipo_muestra": str(nueva_muestra.tipo_muestra),
                "etapa": str(nueva_muestra.etapa),
                "codigo_muestra_interno": nueva_muestra.codigo_muestra_interno,
                "codigo_muestra_producto": nueva_muestra.codigo_muestra_producto,
                "observaciones_muestras": nueva_muestra.observaciones_muestras,
            })

        return JsonResponse({
            "success": True,
            "message": f"{total_guardados} muestra(s) duplicada(s) correctamente.",
            "muestras": muestras_guardadas
        })

    except IntegrityError:
        return JsonResponse({
            "success": False,
            "message": "Error de integridad: posible duplicado."
        }, status=400)

    except Exception:
        return JsonResponse({
            "success": False,
            "message": "Error inesperado en el servidor.",
            "traceback": str(traceback.format_exc())
        }, status=500)


@login_required
@group_required('Administrador')
def sistemas(request):
    titulo="Sistemas"
    sistemas=Sistema.objects.all()
    if request.method == "POST":
        form = sistemaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Sistema creado satisfactoriamente")
            return redirect("sistemas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = sistemaForm() 
    context={
        "titulo":titulo,
        "form":form,
        "sistemas":sistemas,
        
    }
    return render(request, "protocolo_metodos/crear_sistemas.html", context)
#
@login_required
@group_required('Administrador')
def editar_sistemas(request, pk):
    titulo="Editar Sistemas"
    sistemas=Sistema.objects.get(id=pk)
    if request.method == "POST":
        form = sistemaForm(request.POST, instance=sistemas)
        if form.is_valid():
            form.save()
            messages.success(request, "Sistema editado satisfactoriamente")
            return redirect("sistemas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = sistemaForm(instance=sistemas) 
    context={
        "titulo":titulo,
        "form":form,
        "crear_cliente":crear_cliente,
        
    }
    return render(request, "protocolo_metodos/crear_sistemas.html", context)


@login_required
@group_required('Administrador')
def celdas(request):
    titulo="Celdas"
    celdas=Celda.objects.all()
    responsable = User.objects.all
    if request.method == "POST":
        form = CeldaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Celda creada satisfactoriamente")
            return redirect("celdas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = CeldaForm() 
    context={
        "titulo":titulo,
        "form":form,
        "celdas":celdas,
        "responsable":responsable,
        
    }
    return render(request, "protocolo_metodos/celdas.html", context)

@login_required
@group_required('Administrador')
def editar_celdas(request, pk):
    titulo="Editar Celdas"
    responsable = User.objects.all
    celdas=Celda.objects.get(id=pk)
    if request.method == "POST":
        form = CeldaForm(request.POST, instance=celdas)
        if form.is_valid():
            form.save()
            messages.success(request, "Celda editada satisfactoriamente")
            return redirect("celdas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = CeldaForm(instance=celdas) 
    context={
        "titulo":titulo,
        "form":form,
        "celdas":celdas,
        responsable:responsable,
        
    }
    return render(request, "protocolo_metodos/celdas.html", context)

@login_required
@group_required('Administrador')
def metodos(request):
    titulo="Metodos"
    metodos=Metodo.objects.all()
    if request.method == "POST":
        form = MetodoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Método creado satisfactoriamente")
            return redirect("metodos")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = MetodoForm() 
    context={
        "titulo":titulo,
        "form":form,
        "metodos":metodos,
        
    }
    return render(request, "protocolo_metodos/metodos.html", context)

@login_required
@group_required('Administrador')
def editar_metodos(request, pk):
    titulo="Editar metodos"
    metodos=Metodo.objects.get(id=pk)
    if request.method == "POST":
        form = MetodoForm(request.POST, instance=metodos)
        if form.is_valid():
            form.save()
            messages.success(request, "Método editado satisfactoriamente")
            return redirect("metodos")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = MetodoForm(instance=metodos) 
    context={
        "titulo":titulo,
        "form":form,
        "metodos":metodos,
        
    }
    return render(request, "protocolo_metodos/metodos.html", context)

@login_required
@group_required('Administrador')
def tipo_muestra(request):
    titulo="Tipo de Muestras"
    tipo_muestra=Tipo_muestra.objects.all()
    if request.method == "POST":
        form = tipo_muestrasForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de muestra creada satisfactoriamente")
            return redirect("tipo_muestra")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = tipo_muestrasForm() 
    context={
        "titulo":titulo,
        "form":form,
        "tipo_muestra":tipo_muestra,
        
    }
    return render(request, "protocolo_metodos/tipo_muestra.html", context)

@login_required
@group_required('Administrador')
def editar_tipo_muestra(request, pk):
    titulo="Editar Tipo de Muestras"
    tipo_muestra=Tipo_muestra.objects.get(id=pk)
    if request.method == "POST":
        form = tipo_muestrasForm(request.POST, instance=tipo_muestra)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de muestra editada satisfactoriamente")
            return redirect("tipo_muestra")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = tipo_muestrasForm(instance=tipo_muestra) 
    context={
        "titulo":titulo,
        "form":form,
        "tipo_muestra":tipo_muestra,
        
    }
    return render(request, "protocolo_metodos/tipo_muestra.html", context)

@login_required
@group_required('Administrador')
def etapas(request):
    titulo="Etapas"
    etapas=Etapa.objects.all()
    ensayo=Ensayo.objects.all()
    if request.method == "POST":
        form = EtapaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Etapa creada satisfactoriamente")
            return redirect("etapas")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = EtapaForm() 
    context={
        "titulo":titulo,
        "form":form,
        "etapas":etapas,
        "ensayo":ensayo,
        
    }
    return render(request, "protocolo_metodos/etapas.html", context)

@login_required
@group_required('Administrador')
def editar_etapas(request, pk):
    titulo="Editar Etapas de Muestras"
    etapas=Etapa.objects.get(id=pk)
    if request.method == "POST":
        form = EtapaForm(request.POST, instance=etapas)
        if form.is_valid():
            form.save()
            messages.success(request, "Etapa editada satisfactoriamente")
            return redirect("etapas")
        else:
             messages.error(request, "Por favor, revisa los datos ingresados")
    else:
        form = EtapaForm(instance=etapas) 
    context={
        "titulo":titulo,
        "form":form,
        "etapas":etapas,
        
    }
    return render(request, "protocolo_metodos/etapas.html", context)


@login_required
@group_required('Administrador')
def viavilidad_proceso(request):
    titulo="Viavilidad Proceso"
    viavilidad_proceso=ViabilidadProceso.objects.all()
   
    if request.method == "POST":
        form = viavilidad_procesoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro creado satisfactoriamente")
            return redirect("viavilidad_proceso")
        else:
             messages.error(request, "Por favor revisa los datos ingresados")
    else:
        form = viavilidad_procesoForm() 
    context={
        "titulo":titulo,
        "form":form,
        "viavilidad_proceso":viavilidad_proceso,
       
        
    }
    return render(request, "protocolo_metodos/viavilidad_proceso.html", context)

@login_required
@group_required('Administrador')
def editar_viavilidad_proceso(request, pk):
    titulo="Editar Viavilidad Proceso"
    viavilidad_proceso=ViabilidadProceso.objects.get(id=pk)
    if request.method == "POST":
        form = viavilidad_procesoForm(request.POST, instance=viavilidad_proceso)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro editado satisfactoriamente")
            return redirect("viavilidad_proceso")
        else:
             messages.error(request, "Por favor, revisa los datos ingresados")
    else:
        form = viavilidad_procesoForm(instance=viavilidad_proceso) 
    context={
        "titulo":titulo,
        "form":form,
        "viavilidad_proceso":viavilidad_proceso,
        
    }
    return render(request, "protocolo_metodos/viavilidad_proceso.html", context)
































    
        


    
