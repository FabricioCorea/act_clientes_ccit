from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Vista de login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                messages.warning(request, "Tu cuenta está inactiva. Contacta al administrador.")
                return render(request, "auth/login.html")
        except User.DoesNotExist:
            user = None

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            # Redirección según grupo
            if user.groups.filter(name="colector_group").exists():
                return redirect("clientes_colectores")
            elif user.groups.filter(name="estandar_group").exists():
                return redirect("clientes")
            elif user.groups.filter(name__in=["super_admin", "admin_group"]).exists():
                return redirect("gestion")
            else:
                messages.error(request, "No tienes un grupo asignado. Contacta al administrador.")
                return redirect("login")
        else:
            messages.warning(request, "Usuario o contraseña incorrectos.")

    return render(request, "auth/login.html")


# Vista de logout
def user_logout(request):
    auth_logout(request)
    return redirect("login")

# Vista de lista de usuarios con restricciones de grupo
@login_required
def user_list(request):
    is_super_admin_group = request.user.groups.filter(name='super_admin').exists()
    is_admin_group = request.user.groups.filter(name='admin_group').exists()

    # Validar acceso
    if not (is_super_admin_group or is_admin_group):
        messages.error(request, "Acceso no permitido.")
        if request.user.groups.filter(name="colector_group").exists():
            return redirect("clientes_colectores")
        elif request.user.groups.filter(name="estandar_group").exists():
            return redirect("clientes")
        else:
            return redirect("login")

    # Acceso permitido y exclusión del usuario 'colector'
    if is_super_admin_group:
        users = User.objects.prefetch_related('groups').exclude(username="colector")
    elif is_admin_group:
        users = User.objects.prefetch_related('groups').exclude(groups__name="super_admin").exclude(username="colector")

    groups = Group.objects.exclude(name="super_admin")


    return render(request, 'auth/user_list.html', {
        'users': users,
        'groups': groups,
        'is_super_admin_group': is_super_admin_group,
        'is_admin_group': is_admin_group
    })

# Vista para agregar un nuevo usuario
@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        group_name = request.POST.get('group', None)

        if User.objects.filter(username=username).exists():
            messages.warning(request, "El nombre de usuario ya está registrado.")
            return redirect('agregar_usuario')

        new_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if group_name:
            group = Group.objects.get(name=group_name)
            new_user.groups.add(group)

        messages.success(request, "Usuario creado correctamente.")
        return redirect('usuarios')

    return redirect('usuarios')

@csrf_exempt
def toggle_user_status(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        message = "El estado del usuario se cambió correctamente."
        return JsonResponse({"success": True, "new_status": user.is_active, "message": message})
    return JsonResponse({"success": False, "message": "Error al actualizar estado"}, status=400)

# Vista para editar usuario
@login_required
def edit_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        group_name = request.POST.get("group")

        try:
            user = User.objects.get(id=user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if group_name:
                user.groups.clear()
                group = Group.objects.get(name=group_name)
                user.groups.add(group)

            messages.success(request, "Usuario actualizado correctamente.")
        except User.DoesNotExist:
            messages.error(request, "El usuario no existe.")

    return redirect("usuarios")

@login_required
def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.delete()
        message = "Usuario eliminado correctamente."

        return JsonResponse({"success": True, "message": message})
    
    return JsonResponse({"success": False, "message": "Método no permitido."}, status=400)

@login_required
def redireccionar_inicio(request):
    user = request.user
    if user.groups.filter(name="colector_group").exists():
        return redirect("clientes_colectores")
    elif user.groups.filter(name="estandar_group").exists():
        return redirect("clientes_pendientes")
    elif user.groups.filter(name__in=["super_admin", "admin_group"]).exists():
        return redirect("gestion")
    else:
        return redirect("login")  # o una página de error