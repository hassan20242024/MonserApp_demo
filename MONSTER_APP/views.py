from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Aplicaciones.Protocolo_Metodos.models import Protocolos
from Aplicaciones.Protocolo_Muestras.models import Proceso
from django.db.models import Count,Q,Sum
import json
import datetime
from django.conf import settings
settings.DATE_FORMAT
from django.template.defaultfilters import date
from datetime import datetime
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
import calendar
from collections import defaultdict

@login_required
def inicio(request):
    registro_total_protocolo_metodos = Protocolos.objects.count()
    registro_total_protocolo_proceso = Proceso.objects.count()

    años_metodos = Protocolos.objects.annotate(year=ExtractYear('fecha_final')).values_list('year', flat=True).distinct()
    años_procesos = Proceso.objects.annotate(year=ExtractYear('fecha_final')).values_list('year', flat=True).distinct()
    años_disponibles = sorted(set(años_metodos).union(años_procesos), reverse=True)

    context = {
        "registro_total_protocolo_metodos": registro_total_protocolo_metodos,
        "registro_total_protocolo_proceso": registro_total_protocolo_proceso,
        "años_disponibles": años_disponibles,
        "año_actual": datetime.now().year,
        "user_first_name": request.user.first_name,
        # Para cards vacíos de demo
        "registro_desarrollos": 0,
        "registro_estabilidades": 0,
    }
    return render(request, "index-admin.html", context)
@login_required
def inicioAdmin(request):
     return render(request, "index-admin.html")

@login_required
def inicioAdmin(request):
     return render(request, "index-admin.html")


@login_required
def adm_inicio(request):
    registro_total_protocolo_metodos = Protocolos.objects.count()
    registro_total_protocolo_proceso = Proceso.objects.count()

    años_metodos = Protocolos.objects.annotate(year=ExtractYear('fecha_final')).values_list('year', flat=True).distinct()
    años_procesos = Proceso.objects.annotate(year=ExtractYear('fecha_final')).values_list('year', flat=True).distinct()
    años_disponibles = sorted(set(años_metodos).union(años_procesos), reverse=True)

    context = {
        "titulo": "Tablero principal",
        "registro_total_protocolo_metodos": registro_total_protocolo_metodos,
        "registro_total_protocolo_proceso": registro_total_protocolo_proceso,
        "años_disponibles": años_disponibles,
        "año_actual": datetime.now().year,
    }
    return render(request, "inicio.html", context)

@login_required
def chart_finalizados_metodos(request, year):
    dataset = Protocolos.objects \
        .filter(fecha_final__year=year, estado_protocolo="6") \
        .values('fecha_final__month') \
        .annotate(Finalizado=Count('id'))

    data = {
        "categories": [calendar.month_name[entry['fecha_final__month']] for entry in dataset],
        "data": [entry["Finalizado"] for entry in dataset]
    }
    return JsonResponse(data)

@login_required
def chart_finalizados_proceso(request, year):
    dataset = Proceso.objects \
        .filter(fecha_final__year=year, estado_del_proceso="6") \
        .values('fecha_final__month') \
        .annotate(Finalizado=Count('id'))

    data = {
        "categories": [calendar.month_name[entry['fecha_final__month']] for entry in dataset],
        "data": [entry["Finalizado"] for entry in dataset]
    }
    return JsonResponse(data)

@login_required
def chart_motivos_metodos(request, year):
    filtro = Q(fecha_final__year=year)

    dataset = Protocolos.objects.filter(filtro).values("estado_protocolo__estado_motivo").annotate(
        ejecucion=Count("id", filter=Q(estado_protocolo="1")),
        falta_insumos=Count("id", filter=Q(estado_protocolo="2")),
        metodologia=Count("id", filter=Q(estado_protocolo="3")),
        criterio=Count("id", filter=Q(estado_protocolo="4")),
        listado=Count("id", filter=Q(estado_protocolo="5")),
        finalizado=Count("id", filter=Q(estado_protocolo="6")),
    ).exclude(estado_protocolo="7")

    color_map = {
    "(Falta de insumos)": "#f39c12",       
    "(Problemas de metodología)": "#e74c3c", 
    "(Muestras no cumplen parámetros)": "#8e44ad", 
    "(Ingresado)": "#3498db",             
    "(Culminado)": "#2ecc71",      
    "(En ejecución)": "#d87cae",    
    "(Sin motivo)": "#95a5a6"                                  
}

    data_pie = []

    for d in dataset:
        nombre = d['estado_protocolo__estado_motivo'] or "Sin motivo"
        total = (
            d['ejecucion'] +
            d['falta_insumos'] +
            d['metodologia'] +
            d['criterio'] +
            d['listado'] +
            d['finalizado']
        )
        color = color_map.get(nombre, "#34495e")
        data_pie.append({'name': nombre, 'y': total, 'color': color})

    return JsonResponse({
        'chart': {
            'type': 'pie',
            'height': '60%'  # Ajusta el alto si quieres más espacio vertical
        },
        'title': {'text': ''},
        'tooltip': {
            'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        'accessibility': {
            'point': {'valueSuffix': '%'}
        },
        'plotOptions': {
            'pie': {
                #'startAngle': -90,
               # 'endAngle': 90,
               # 'center': ['50%', '75%'],
                'innerSize': '50%',  # Esto hace que sea tipo "donut"
                'dataLabels': {
                    'enabled': True,
                    'defer': False,
                    'style': {
                        'fontSize': '12px'
                    },
                 'format': '<b>{point.name}</b>: {point.y} ({point.percentage:.1f} %)'
                }
            }
        },
        'series': [{
            'name': 'Protocolos',
            'colorByPoint': False,
            'data': data_pie
        }]
    })


@login_required
def chart_motivos_proceso(request, year):
    filtro = Q(fecha_final__year=year)

    dataset = Proceso.objects.filter(filtro).values("estado_del_proceso__estado_motivo").annotate(
        listado=Count("id", filter=Q(estado_del_proceso="5")),
        finalizado=Count("id", filter=Q(estado_del_proceso="6")),
        falta_insumos=Count("id", filter=Q(estado_del_proceso="2")),
        metodologia=Count("id", filter=Q(estado_del_proceso="3")),
        criterio=Count("id", filter=Q(estado_del_proceso="4")),
        ejecucion=Count("id", filter=Q(estado_del_proceso="1")),
    ).exclude(estado_del_proceso="7")

    color_map = {
    "(Falta de insumos)": "#f39c12",       
    "(Problemas de metodología)": "#e74c3c", 
    "(Muestras no cumplen parámetros)": "#8e44ad", 
    "(Ingresado)": "#3498db",             
    "(Culminado)": "#2ecc71",      
    "(En ejecución)": "#d87cae",    
    "(Sin motivo)": "#95a5a6"                                  
}

    data_dict = defaultdict(int)

    for d in dataset:
        motivo = d['estado_del_proceso__estado_motivo'] or "Sin motivo"
        total = (
            d['listado'] +
            d['finalizado'] +
            d['falta_insumos'] +
            d['metodologia'] +
            d['criterio'] +
            d['ejecucion']
        )
        data_dict[motivo] += total

    data_pie = []
    for k, v in data_dict.items():
        color = color_map.get(k, "#34495e")
        data_pie.append({'name': k, 'y': v, 'color': color})

    return JsonResponse({
        'chart': {
            'type': 'pie',
            'height': '60%'
        },
        'title': {'text': ''},  # Si no quieres título
        'tooltip': {
            'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        'accessibility': {
            'point': {'valueSuffix': '%'}
        },
        'plotOptions': {
            'pie': {
                'innerSize': '50%',  # Hace que sea tipo DONA
                'allowPointSelect': True,
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': True,
                    'style': {
                        'fontSize': '12px'
                    },
                    'format': '<b>{point.name}</b>: {point.y} ({point.percentage:.1f} %)'
                }
            }
        },
        'series': [{
            'name': 'Procesos',
            'colorByPoint': False,
            'data': data_pie
        }]
    })







