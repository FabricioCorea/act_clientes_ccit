from django.urls import resolve

def active_menu(request):
    """
    Retorna el nombre del menú activo según la URL.
    """
    url_name = resolve(request.path_info).url_name  # Obtiene el nombre de la URL actual

    # Definir las secciones principales y sus subrutas
    active_pages = {
        "inicio": ["inicio"],
        "clientes": ["clientes", "clientes_pendientes", "clientes_seguimiento", "clientes_sin_contestar", "clientes_sin_actualizar", "clientes_actualizados"],
        "clientes_colectores": ["clientes_colectores", "clientes_colectores_completados", "clientes_colectores_actualizados"],
        "clientes_reportados": ["clientes_reportados"],
        "usuarios": ["usuarios", "agregar_usuario", "editar_usuario", "eliminar_usuario"],
        "dashboard_reportes": ["dashboard_reportes", "seguimiento_comparativa"], 
        "gestion": ["gestion", "clientes_todos_gestion", "clientes_para_colectores_gestion", "clientes_pendientes_gestion", "clientes_seguimiento_gestion", "clientes_actualizados_gestion"],
    }

    # Buscar qué sección principal coincide con la URL actual
    active_section = None
    for key, urls in active_pages.items():
        if url_name in urls:
            active_section = key
            break

    return {"active_page": active_section}
