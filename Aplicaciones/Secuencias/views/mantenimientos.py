from django.shortcuts import render, redirect, get_object_or_404
from ..models import  Sistema, usuario_validar, Lavado_buzo
from ..forms import LavadoBuzoForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime, timedelta
import datetime
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta, MO
import traceback

@login_required
def mantenimientos_periodicos(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    sistema=Sistema.objects.all()
    date_joined = datetime.datetime.now()
    formatedDate = date_joined.strftime("%Y-%m-%d %H:%M:%S")
    progrmado = date_joined + datetime.timedelta(days=30)
    programados=Lavado_buzo.objects.filter(fecha_lavado_buzo=progrmado)
    realizado_por=usuario_validar.objects.filter(usuario=request.user)
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
        "sistema":sistema,
        "realizado_por":realizado_por,
        "programados":programados,
        formatedDate:formatedDate
    }
    return render(request, "secuencias/mantenimientos_periodicos.html", context)

@login_required
def mantenimientos_buzos_realizados(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/mantenimientos_buzos_realizados.html", context)

@login_required
def mantenimientos_celdas_realizados(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/mantenimientos_celdas_realizados.html", context)

@login_required
def mantenimientos_test_realizados(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/mantenimientos_test_realizados.html", context)

@login_required
def mantenimientos_preventivo_realizado(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/mantenimientos_preventivo_realizado.html", context)

@login_required
def calificaciones_realizadas(request):
    titulo="Mantenimientos Periódicos"
    lavado_buzo=Lavado_buzo.objects.all()
    context={
        "titulo":titulo,
        "lavado_buzo":lavado_buzo,
    }
    return render(request, "secuencias/calificaciones_realizadas.html", context)


def get_badge_class(fecha, alerta_inf, alerta_sup, status, realizado=False, tipo=None):
    if realizado:
        return "badge badge-success"

    today = datetime.date.today()

    if tipo in ["mantenimiento", "calificacion"]:
        if not fecha:
            return "badge badge-secondary"

        # Extraer año y mes ignorando los días
        fecha_programada_year = fecha.year
        fecha_programada_month = fecha.month
        hoy_year = today.year
        hoy_month = today.month

        # Diferencia en meses entre hoy y la fecha programada
        diff_meses = (fecha_programada_year - hoy_year) * 12 + (fecha_programada_month - hoy_month)

        if diff_meses < 0:
            # Si ya pasó el mes programado -> rojo
            return "badge badge-danger"
        elif diff_meses == 0:
            # Mismo mes que la fecha programada -> amarillo
            return "badge badge-warning text-black"
        elif diff_meses == 1:
            # Falta exactamente 1 mes -> verde claro
            return "badge badge-warning-light"
        else:
            # Faltan más de 1 mes -> gris
            return "badge badge-secondary"

    # Para los demás tipos, lógica original
    if alerta_inf and fecha and alerta_inf > today:
        return "badge badge-secondary"
    elif alerta_inf and alerta_sup and alerta_inf <= today <= fecha:
        return "badge badge-warning text-black"
    elif fecha and alerta_sup and fecha <= today <= alerta_sup:
        return "badge badge-warning text-black"
    elif alerta_sup and today > alerta_sup:
        return "badge badge-danger"

    return "badge badge-secondary"
    

@login_required
def get_lavado_buzo_data(request):
    data = []
    today = datetime.date.today()
    is_admin = request.user.groups.filter(name='Administrador').exists()
    items = Lavado_buzo.objects.filter(status="Programado", status_celda="Programado")

    for item in items:
        # Construcción de badges y checkboxes para cada tipo (lavado, celdas, etc.)
        buzo_badge = get_badge_class(
            item.fecha_lavado_buzo,
            item.fecha_alerta_inferior,
            item.fecha_alerta_superior,
            item.status,
            item.status == "Realizado"
        )
        buzo_fecha = item.fecha_lavado_buzo.strftime("%Y-%m-%d") if item.fecha_lavado_buzo else ''
        buzo_checkbox = f'<input type="checkbox" name="item" value="{item.id}" title="Lavado de buzos">'
        lav_buz_html = f'<small class="{buzo_badge}"><i class="far fa-clock"></i> {buzo_fecha}</small> {buzo_checkbox}'

        cel_badge = get_badge_class(
            item.fecha_lavado_celda,
            item.fecha_alerta_inferior_celda,
            item.fecha_alerta_superior_celda,
            item.status_celda,
            item.status_celda == "Realizado"
        )
        cel_fecha = item.fecha_lavado_celda.strftime("%Y-%m-%d") if item.fecha_lavado_celda else ''
        cel_checkbox = f'<input type="checkbox" name="itemCelda" value="{item.id}" title="Lavado de celda">'
        lav_celd_html = f'<small class="{cel_badge}"><i class="far fa-clock"></i> {cel_fecha}</small> {cel_checkbox}'

        test_badge = get_badge_class(
            item.fecha_test_diagnostico,
            item.fecha_alerta_inferior_test,
            item.fecha_alerta_superior_test,
            item.status_test,
            item.status_test == "Realizado"
        )
        test_fecha = item.fecha_test_diagnostico.strftime("%Y-%m-%d") if item.fecha_test_diagnostico else ''
        test_checkbox = f'<input type="checkbox" name="itemTest" value="{item.id}" title="Test diagnóstico">'
        test_html = f'<small class="{test_badge}"><i class="far fa-clock"></i> {test_fecha}</small> {test_checkbox}'

        mant_badge = get_badge_class(
            item.fecha_mantenimiento,
            item.fecha_alerta_inferior_mantenimiento,
            item.fecha_alerta_superior_mantenimiento,
            item.status_mantenimiento,
            item.status_mantenimiento == "Realizado",
            tipo="mantenimiento"

        )
        mant_fecha = item.fecha_mantenimiento.strftime("%Y-%m") if item.fecha_mantenimiento else ''
        mant_checkbox = f'<input type="checkbox" name="itemMantenimiento" value="{item.id}" title="Mantenimiento">'
        maintenance_html = f'<small class="{mant_badge}"><i class="far fa-clock"></i> {mant_fecha}</small> {mant_checkbox}'

        calif_badge = get_badge_class(
            item.fecha_calificacion,
            item.fecha_alerta_inferior_calificacion,
            item.fecha_alerta_superior_calificacion,
            item.status_calificacion,
            item.status_calificacion == "Realizado",
            tipo="calificacion"
        )
        calif_fecha = item.fecha_calificacion.strftime("%Y-%m") if item.fecha_calificacion else ''
        calif_checkbox = f'<input type="checkbox" name="itemCalificacion" value="{item.id}" title="Calificación">'
        calif_html = f'<small class="{calif_badge}"><i class="far fa-clock"></i> {calif_fecha}</small> {calif_checkbox}'
        sistema_nombre = f"<div style='position: relative; display: inline-block;'>{item.sistema.nombre}"
        if item.sistema.condicion == "Pasivo":
           sistema_nombre += ' <span class="text-danger text-sm fw-bold">(Fuera de Servicio)</span>'
        row = {
            "id": item.id,
            "sistema": sistema_nombre,
            "lavado_buzos": lav_buz_html,
            "lavado_celdas": lav_celd_html,
            "test_diagnostico": test_html,
            "mantenimiento": maintenance_html,
            "calificacion": calif_html,
        }

        if is_admin:
            row["editar"] = (
               f"<button type='button' class='btn btn-sm btn-outline-primary' "
               f"onclick='editarRegistro({item.id})'>"
               f"<i class='fa fa-edit text-secondary fa-lg'></i>"
                "</button>"
            )
        else:
            row["editar"] = ""
        data.append(row)
    return JsonResponse({"data": data})

@login_required
def mantenimientos_buzos_Check_form(request):
    if request.method == "POST":
        try:
            # Recolectar los checks del formulario
            ids_buzos = request.POST.getlist("item")
            ids_celdas = request.POST.getlist("itemCelda")
            ids_test = request.POST.getlist("itemTest")
            ids_mantenimiento = request.POST.getlist("itemMantenimiento")
            ids_calificacion = request.POST.getlist("itemCalificacion")

            user = User.objects.get(username=request.user)

            # Lavado de Buzos
            for id in ids_buzos:
                obj = Lavado_buzo.objects.get(pk=id)
                obj.status = Lavado_buzo.Status.PROGRAMADO
                obj.fecha_lavado_buzo = datetime.datetime.now() + datetime.timedelta(days=30)
                obj.fecha_alerta_inferior = datetime.datetime.now() + datetime.timedelta(days=27)
                obj.fecha_alerta_superior = datetime.datetime.now() + datetime.timedelta(days=33)
                obj.save()

                obj.pk = None
                obj.status = Lavado_buzo.Status.REALIZADO
                obj.status_celda = Lavado_buzo.Status_celda.PENDIENTE
                obj.status_test = Lavado_buzo.Status_test.PENDIENTE
                obj.status_mantenimiento = Lavado_buzo.Status_mantenimiento.PENDIENTE
                obj.status_calificacion = Lavado_buzo.Status_calificacion.PENDIENTE
                obj.fecha_lavado_buzo = datetime.datetime.now()
                obj.fecha_lavado_celda = None
                obj.fecha_test_diagnostico = None
                obj.realizado_por = user
                obj.save()

            # Lavado de Celdas
            for id in ids_celdas:
                obj = Lavado_buzo.objects.get(pk=id)
                obj.status_celda = Lavado_buzo.Status_celda.PROGRAMADO
                obj.fecha_lavado_celda = datetime.datetime.now() + datetime.timedelta(days=30)
                obj.fecha_alerta_inferior_celda = datetime.datetime.now() + datetime.timedelta(days=27)
                obj.fecha_alerta_superior_celda = datetime.datetime.now() + datetime.timedelta(days=33)
                obj.save()

                obj.pk = None
                obj.status_celda = Lavado_buzo.Status_celda.REALIZADO
                obj.status = Lavado_buzo.Status.PENDIENTE
                obj.status_test = Lavado_buzo.Status_test.PENDIENTE
                obj.status_mantenimiento = Lavado_buzo.Status_mantenimiento.PENDIENTE
                obj.status_calificacion = Lavado_buzo.Status_calificacion.PENDIENTE
                obj.fecha_lavado_celda = datetime.datetime.now()
                obj.fecha_lavado_buzo = None
                obj.fecha_test_diagnostico = None
                obj.realizado_por_celda = user
                obj.save()

            # Test Diagnóstico
            for id in ids_test:
                obj = Lavado_buzo.objects.get(pk=id)
                obj.status_test = Lavado_buzo.Status_test.PROGRAMADO
                obj.fecha_test_diagnostico = datetime.datetime.now() + datetime.timedelta(days=30)
                obj.fecha_alerta_inferior_test = datetime.datetime.now() + datetime.timedelta(days=27)
                obj.fecha_alerta_superior_test = datetime.datetime.now() + datetime.timedelta(days=33)
                obj.save()

                obj.pk = None
                obj.status_test = Lavado_buzo.Status_test.REALIZADO
                obj.status = Lavado_buzo.Status.PENDIENTE
                obj.status_celda = Lavado_buzo.Status_celda.PENDIENTE
                obj.status_mantenimiento = Lavado_buzo.Status_mantenimiento.PENDIENTE
                obj.status_calificacion = Lavado_buzo.Status_calificacion.PENDIENTE
                obj.fecha_test_diagnostico = datetime.datetime.now()
                obj.fecha_lavado_buzo = None
                obj.fecha_lavado_celda = None
                obj.realizado_por_test = user
                obj.save()

            # Mantenimiento Preventivo
            for id in ids_mantenimiento:
                obj = Lavado_buzo.objects.get(pk=id)
                obj.status_mantenimiento = Lavado_buzo.Status_mantenimiento.PROGRAMADO
                obj.fecha_mantenimiento = datetime.datetime.now() + relativedelta(months=6)
                obj.fecha_alerta_inferior_mantenimiento = datetime.datetime.now() + relativedelta(months=5)
                obj.fecha_alerta_superior_mantenimiento = datetime.datetime.now() + relativedelta(months=7)
                obj.save()

                obj.pk = None
                obj.status_mantenimiento = Lavado_buzo.Status_mantenimiento.REALIZADO
                obj.status = Lavado_buzo.Status.PENDIENTE
                obj.status_celda = Lavado_buzo.Status_celda.PENDIENTE
                obj.status_test = Lavado_buzo.Status_test.PENDIENTE
                obj.status_calificacion = Lavado_buzo.Status_calificacion.PENDIENTE
                obj.fecha_mantenimiento = datetime.datetime.now()
                obj.fecha_lavado_buzo = None
                obj.fecha_lavado_celda = None
                obj.fecha_test_diagnostico = None
                obj.realizado_por_mantenimiento = user
                obj.save()

            # Calificación
            for id in ids_calificacion:
                obj = Lavado_buzo.objects.get(pk=id)
                obj.status_calificacion = Lavado_buzo.Status_calificacion.PROGRAMADO
                obj.fecha_calificacion = datetime.datetime.now() + relativedelta(months=12)
                obj.fecha_alerta_inferior_calificacion = datetime.datetime.now() + relativedelta(months=11)
                obj.fecha_alerta_superior_calificacion = datetime.datetime.now() + relativedelta(months=13)
                obj.save()

                obj.pk = None
                obj.status_calificacion = Lavado_buzo.Status_calificacion.REALIZADO
                obj.status = Lavado_buzo.Status.PENDIENTE
                obj.status_celda = Lavado_buzo.Status_celda.PENDIENTE
                obj.status_test = Lavado_buzo.Status_test.PENDIENTE
                obj.status_mantenimiento = Lavado_buzo.Status_mantenimiento.PENDIENTE
                obj.fecha_calificacion = datetime.datetime.now()
                obj.fecha_lavado_buzo = None
                obj.fecha_lavado_celda = None
                obj.fecha_test_diagnostico = None
                obj.realizado_por_calificacion = user
                obj.save()

            return JsonResponse({"success": True, "message": "Registros actualizados exitosamente"})

        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({"success": False, "message": "Error interno del servidor"}, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

@login_required
def crear_lavado_buzo_ajax(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        form = LavadoBuzoForm(data)

        if form.is_valid():
            lavado = form.save(commit=False)

            # Fechas ingresadas
            fb = form.cleaned_data.get('fecha_lavado_buzo')
            fc = form.cleaned_data.get('fecha_lavado_celda')
            ft = form.cleaned_data.get('fecha_test_diagnostico')
            fm = form.cleaned_data.get('fecha_mantenimiento')
            fca = form.cleaned_data.get('fecha_calificacion')

            # Calcular alertas
            if fb:
                lavado.fecha_alerta_inferior = fb - timedelta(days=3)
                lavado.fecha_alerta_superior = fb + timedelta(days=3)
            if fc:
                lavado.fecha_alerta_inferior_celda = fc - timedelta(days=3)
                lavado.fecha_alerta_superior_celda = fc + timedelta(days=3)
            if ft:
                lavado.fecha_alerta_inferior_test = ft - timedelta(days=3)
                lavado.fecha_alerta_superior_test = ft + timedelta(days=3)
            if fm:
                lavado.fecha_alerta_inferior_mantenimiento = fm - relativedelta(months=1)
                lavado.fecha_alerta_superior_mantenimiento = fm + relativedelta(months=1)
            if fca:
                lavado.fecha_alerta_inferior_calificacion = fca - relativedelta(months=1)
                lavado.fecha_alerta_superior_calificacion = fca + relativedelta(months=1)

            # Asignar status por defecto
            lavado.status = Lavado_buzo.Status.PROGRAMADO
            lavado.status_celda = Lavado_buzo.Status_celda.PROGRAMADO
            lavado.status_test = Lavado_buzo.Status_test.PROGRAMADO
            lavado.status_mantenimiento = Lavado_buzo.Status_mantenimiento.PROGRAMADO
            lavado.status_calificacion = Lavado_buzo.Status_calificacion.PROGRAMADO

            lavado.save()
            return JsonResponse({'message': 'Lavado registrado correctamente'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@login_required
def editar_lavado_buzo(request, pk):
    if request.method == 'PUT':
        try:
            lavado = Lavado_buzo.objects.get(pk=pk)
        except Lavado_buzo.DoesNotExist:
            return JsonResponse({'error': 'No se encontró el registro'}, status=404)

        data = json.loads(request.body)
        form = LavadoBuzoForm(data, instance=lavado)

        if form.is_valid():
            lavado = form.save(commit=False)

            # Fechas ingresadas
            fb = form.cleaned_data.get('fecha_lavado_buzo')
            fc = form.cleaned_data.get('fecha_lavado_celda')
            ft = form.cleaned_data.get('fecha_test_diagnostico')
            fm = form.cleaned_data.get('fecha_mantenimiento')
            fca = form.cleaned_data.get('fecha_calificacion')

            # Recalcular alertas
            if fb:
                lavado.fecha_alerta_inferior = fb - timedelta(days=3)
                lavado.fecha_alerta_superior = fb + timedelta(days=3)
            else:
                lavado.fecha_alerta_inferior = None
                lavado.fecha_alerta_superior = None

            if fc:
                lavado.fecha_alerta_inferior_celda = fc - timedelta(days=3)
                lavado.fecha_alerta_superior_celda = fc + timedelta(days=3)
            else:
                lavado.fecha_alerta_inferior_celda = None
                lavado.fecha_alerta_superior_celda = None

            if ft:
                lavado.fecha_alerta_inferior_test = ft - timedelta(days=3)
                lavado.fecha_alerta_superior_test = ft + timedelta(days=3)
            else:
                lavado.fecha_alerta_inferior_test = None
                lavado.fecha_alerta_superior_test = None

            if fm:
                lavado.fecha_alerta_inferior_mantenimiento = fm - relativedelta(months=1)
                lavado.fecha_alerta_superior_mantenimiento = fm + relativedelta(months=1)
            else:
                lavado.fecha_alerta_inferior_mantenimiento = None
                lavado.fecha_alerta_superior_mantenimiento = None

            if fca:
                lavado.fecha_alerta_inferior_calificacion = fca - relativedelta(months=1)
                lavado.fecha_alerta_superior_calificacion = fca + relativedelta(months=1)
            else:
                lavado.fecha_alerta_inferior_calificacion = None
                lavado.fecha_alerta_superior_calificacion = None

            lavado.save()
            return JsonResponse({'message': 'Registros actualizados exitosamente'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def lavado_buzo_detalle(request, pk):
    try:
        item = Lavado_buzo.objects.get(pk=pk)
    except Lavado_buzo.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro'}, status=404)

    data = {
        "id": item.id,
        "sistema": item.sistema.id,  
        "fecha_lavado_buzo": item.fecha_lavado_buzo.isoformat() if item.fecha_lavado_buzo else None,
        "fecha_lavado_celda": item.fecha_lavado_celda.isoformat() if item.fecha_lavado_celda else None,
        "fecha_test_diagnostico": item.fecha_test_diagnostico.isoformat() if item.fecha_test_diagnostico else None,
        "fecha_mantenimiento": item.fecha_mantenimiento.isoformat() if item.fecha_mantenimiento else None,
        "fecha_calificacion": item.fecha_calificacion.isoformat() if item.fecha_calificacion else None,
        "observaciones": item.observaciones,
    }
    return JsonResponse(data)
