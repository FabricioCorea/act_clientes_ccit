from django.contrib import admin
from django.urls import path
from clientes import views as vistasClientes
from usuarios import views as vistasUsuarios
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vistasUsuarios.redireccionar_inicio, name='inicio'),

  
    path('clientes/pendientes/', vistasClientes.clientes_pendientes, name='clientes'),
    path('clientes/seguimiento/', vistasClientes.clientes_seguimiento, name='clientes_seguimiento'),
    path('clientes/nocontesto/', vistasClientes.clientes_sin_contestar, name='clientes_sin_contestar'),
    path('clientes/sinactualizar/', vistasClientes.clientes_sin_actualizar, name='clientes_sin_actualizar'),
    path('clientes/actualizados/', vistasClientes.clientes_actualizados, name='clientes_actualizados'),

    
    path('clientes/contactados/', vistasClientes.clientes_reportados, name='clientes_reportados'),
    path("clientes/exportar_excel/", vistasClientes.exportar_clientes_reportados_excel, name="exportar_clientes_reportados_excel"),

    path('clientes/reportar/', vistasClientes.reportar_cliente, name='reportar_cliente'),
    path('crear_estado_reporte/', vistasClientes.crear_estado_reporte, name='crear_estado_reporte'),
    path('actualizar-estado-cliente/', vistasClientes.actualizar_estado_cliente, name='actualizar_estado_cliente'),

    path('clientes/dashboard/', vistasClientes.dashboard_reportes, name='dashboard_reportes'),
    path('clientes/seguimiento-comparativa/', vistasClientes.seguimiento_comparativa, name='seguimiento_comparativa'),
    path('exportar-seguimiento-categoria/', vistasClientes.exportar_seguimiento_categoria, name='exportar_seguimiento_categoria'),



    path('gestion/sin-asignar/', vistasClientes.clientes_sin_asignar_view, name='gestion'),
    path('gestion/actualizados/', vistasClientes.clientes_actualizados_view, name='clientes_actualizados_gestion'),
    path('gestion/seguimiento/', vistasClientes.clientes_en_seguimiento_view, name='clientes_seguimiento_gestion'),
    path('gestion/pendientes/', vistasClientes.clientes_pendientes_view, name='clientes_pendientes_gestion'),
    path('gestion/colectores/', vistasClientes.clientes_para_colectores_view, name='clientes_para_colectores_gestion'),
    path('gestion/todos/', vistasClientes.clientes_todos_view, name='clientes_todos_gestion'),
    


    path('gestion/asignacion', vistasClientes.asignar_cliente, name='asignacion'),
    

    path('gestion/asignar-por-estado', vistasClientes.asignar_clientes_por_estado, name='asignar_clientes_por_estado'),
    path('gestion/desasignar-por-estado', vistasClientes.desasignar_clientes_por_estado, name='desasignar_clientes_por_estado'),

    path('reasignar_cliente_colector/', vistasClientes.reasignar_cliente_colector, name='reasignar_cliente_colector'),


    path('colectores/pendientes/', vistasClientes.clientes_colectores_pendientes, name='clientes_colectores'),
    path('colectores/completados/', vistasClientes.clientes_colectores_completados, name='clientes_colectores_completados'),
    path('colectores/actualizados/', vistasClientes.clientes_colectores_actualizados, name='clientes_colectores_actualizados'),

    path('clientes/editar/', vistasClientes.editar_cliente, name='editar_cliente'),


    path('clientes/importar/', vistasClientes.importar_clientes, name='importar_clientes'),
    path('exportar_clientes/', vistasClientes.exportar_clientes, name='exportar_clientes'),




    path('login/', vistasUsuarios.user_login, name='login'),  
    path('logout/', vistasUsuarios.user_logout, name='logout'),
    


    path('usuarios/', vistasUsuarios.user_list, name='usuarios'), 
    path('usuarios/cambiar_estado/<int:user_id>/', vistasUsuarios.toggle_user_status, name='toggle_user_status'),
    path('usuarios/agregar/', vistasUsuarios.add_user, name='agregar_usuario'),
    path('usuarios/editar/', vistasUsuarios.edit_user, name='editar_usuario'),
    path('usuarios/eliminar/<int:user_id>/', vistasUsuarios.delete_user, name='eliminar_usuario'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)