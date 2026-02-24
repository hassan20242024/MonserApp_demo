from django.urls import path
from . import views

urlpatterns=[
path('lavado/ajax/', views.crear_lavado_buzo_ajax, name='lavado_buzo_ajax'),
path('get_lavado_buzo_data/', views.get_lavado_buzo_data, name='get_lavado_buzo_data'),
path('ruta-api-editar/<int:pk>/', views.editar_lavado_buzo, name='editar_lavado_buzo'),
path('ruta-api-detalle/<int:pk>/', views.lavado_buzo_detalle, name='detalle_lavado_buzo'),
path('retornar_estado_registrada/', views.retornar_estado_registrada, name='retornar_estado_registrada'),
path("secuencias_invalidadas/",views.secuencias_invalidadas, name="secuencias_invalidadas"),
path("crear_secuencias_en_curso/listado_secuencias_invalidas/",views.listado_secuencias_invalidas, name="(listado_secuencias_invalidas)"),
path('listado_sistemas/', views.listado_sistemas, name='listado_sistemas'),
path('chart-data-json/', views.chart_data_json, name='chart-data-json'),
path('listado_muestras/', views.listado_muestras, name='listado_muestras'),
path("registro_inicial_de_secuencias/",views.registro_inicial_de_secuencias, name="registro_inicial_de_secuencias"),
path('cambiar_estado_invalida/', views.cambiar_estado_invalida, name='cambiar_estado_invalida'),
path('crear_secuencias_protocolo_metodo/', views.crear_secuencias_protocolo_metodo, name='crear_secuencias_protocolo_metodo'),
path("crear_secuencias_en_curso/listado_secuencias_registradas/",views.listado_secuencias_registradas, name="(listado_secuencias_registradas)"),

#Select encadenados
path('ajax/parametros/<int:protocolo_id>/', views.obtener_parametros_por_protocolo, name='obtener_parametros'),
path('ajax/muestras/<int:proceso_id>/', views.obtener_muestras_por_proceso, name='obtener_muestras'),
path('ajax/parametros/<int:protocolo_id>/', views.get_parametros_por_protocolo, name='get_parametros_por_protocolo'),

#editar secuencias
path('editar_secuencia/<int:secuencia_id>/', views.editar_secuencias_protocolo_metodo, name='editar_secuencia'),
  
#Duplicar secuencias Parametro
path('duplicar_secuencia_parametro/<int:secuencia_id>/', views.duplicar_secuencia_parametro, name='duplicar_secuencia_parametro'),

#Duplicar secuencias Muestras
path('duplicar_secuencia_muestras/<int:secuencia_id>/', views.duplicar_secuencia_muestras, name='duplicar_secuencia_muestras'),

path("api/secuencias/<int:pk>/actualizar/", views.actualizar_secuencia, name="actualizar_secuencia"),
path('revertir_estado_a_impresa/', views.revertir_estado_a_impresa, name='revertir_estado_a_impresa'),
path('revertir_estado_a_reportada/', views.revertir_estado_a_reportada, name='revertir_estado_a_reportada'),
path('revertir_estado_a_revisada/', views.revertir_estado_a_revisada, name='revertir_estado_a_revisada'),
path('revertir_estado_a_registrada/', views.revertir_estado_a_registrada, name='revertir_estado_a_registrada'),
path('cambiar_estado_revisar/', views.cambiar_estado_revisar, name='cambiar_estado_revisar'),
path('cambiar_estado_reportar/', views.cambiar_estado_reportar, name='cambiar_estado_reportar'),
path('cambiar_estado_impresa/', views.cambiar_estado_impresa, name='cambiar_estado_impresa'),
path('cambiar_estado_auditada/', views.cambiar_estado_auditada, name='cambiar_estado_auditada'),
path("proceso_secuencias_en_curso/listado_secuencias_validadas/",views.listado_secuencias_validadas, name="(listado_secuencias_validadas)"),
path("secuencias_en_curso_protocolo_metodo/listado_protocolos_metodos/",views.listado_protocolos_metodos, name="listado_protocolos_metodos"),
path("secuencias_en_curso_protocolo_metodo/listado_parametros/",views.listado_parametros, name="listado_parametros"),
path("secuencias_en_curso_protocolo_metodo/listado_parametros_por_id/<int:pk>/", views.listado_parametros_por_id,name="listado_parametros_por_id"),
path("proceso_secuencias_en_curso/",views.proceso_secuencias_en_curso, name="proceso_secuencias_en_curso"),
path("chart_js_proceso_secuencias_en_curso/",views.chart_js_proceso_secuencias_en_curso, name="chart_js_proceso_secuencias_en_curso"),
path("mantenimientos_periodicos/",views.mantenimientos_periodicos, name="mantenimientos_periodicos"),
path("mantenimientos_buzos_realizados/",views.mantenimientos_buzos_realizados, name="mantenimientos_buzos_realizados"),
path("mantenimientos_celdas_realizados/",views.mantenimientos_celdas_realizados, name="mantenimientos_celdas_realizados"),
path("mantenimientos_test_realizados/",views.mantenimientos_test_realizados, name="mantenimientos_test_realizados"),
path("mantenimientos_preventivo_realizado/",views.mantenimientos_preventivo_realizado, name="mantenimientos_preventivo_realizado"),
path("calificaciones_realizadas/",views.calificaciones_realizadas, name="calificaciones_realizadas"),
path("mantenimientos_buzos_Check_form/", views.mantenimientos_buzos_Check_form, name="mantenimientos_buzos_Check_form"),
]