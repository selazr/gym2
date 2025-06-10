from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import AdminUserCreationForm, AdminUserUpdateForm


User = get_user_model()

# Función para verificar si el usuario es administrador
def is_admin(user):
    """Función para verificar si el usuario es administrador"""
    return user.is_authenticated and user.role == 'admin'

# Vista para listar usuarios
@login_required
@user_passes_test(is_admin)
def user_list(request):
    """Lista de usuarios del gimnasio (solo visible para administradores)"""
    users = User.objects.all()
    return render(request, 'admin_gym/user_list.html', {'users': users})

# Vista para crear un usuario
@login_required
@user_passes_test(is_admin)
def create_user(request):
    """Permite a un administrador registrar nuevos usuarios"""
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado exitosamente.")
            return redirect('admin_gym:user_list')
    else:
        form = AdminUserCreationForm()

    return render(request, 'admin_gym/create_user.html', {'form': form})

# Vista para actualizar un usuario
@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    """Permite a un administrador editar un usuario (incluyendo su rol)"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('admin_gym:user_list')
    else:
        form = AdminUserUpdateForm(instance=user)

    return render(request, 'admin_gym/update_user.html', {'form': form, 'user': user})

# Vista para eliminar un usuario
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    """Permite a un administrador eliminar un usuario"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('admin_gym:user_list')

    return render(request, 'admin_gym/delete_user.html', {'user': user})
