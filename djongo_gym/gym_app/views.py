from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, SimpleRutinaForm, UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages import get_messages

@login_required
def profile_view(request):
    """Permite al usuario ver y actualizar sus datos personales."""

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


@login_required
def change_password(request):
    """Permite al usuario cambiar su contraseña."""

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión después del cambio de contraseña
            messages.success(request, "Tu contraseña ha sido actualizada correctamente.")
            return redirect('profile')
        else:
            messages.error(request, "Hubo un error al cambiar la contraseña. Intenta nuevamente.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})

def register(request):
    """
    Maneja el registro de nuevos usuarios.

    Si la solicitud es POST, intenta registrar al usuario con los datos enviados.
    Si el registro es exitoso, el usuario es autenticado e inicia sesión automáticamente.
    Si hay errores en el formulario, muestra un mensaje de error.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponse: Renderiza la plantilla 'register.html' con el formulario.
    """
    if request.method == 'POST':
        # Crear formulario de registro con los datos enviados
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario en la base de datos
            user = form.save()
            # Iniciar sesión automáticamente después del registro
            login(request, user)
            messages.success(request, 'Register complete sussefuly')
            # Redirigir al usuario a la página principal
            return redirect('home')
        else:
            messages.error(request, 'Error doing the register. Please fix the errors')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """
    Maneja el inicio de sesión de usuarios.

    Si la solicitud es POST, verifica las credenciales del usuario. 
    Si son válidas, inicia sesión y redirige al usuario a la página principal.
    Si las credenciales son incorrectas, muestra un mensaje de error genérico.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponse: Renderiza la plantilla 'login.html' con el formulario.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            

            try:
                user = get_user_model().objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, 'Conexión exitosa')

                    # Redirigir según el tipo de usuario
                    if user.role == 'trainer':
                        # Redirigir al dashboard del entrenador usando namespacae
                        return redirect('trainer:dashboard')  
                    elif user.role == 'admin':
                        return redirect('admin_gym:user_list') 
                    elif user.role == 'director':
                        return redirect('gerente:user_list')
                    else:
                        return redirect('home')  # Redirigir al dashboard del usuario normal

            except get_user_model().DoesNotExist:
                messages.error(request, 'Claves de acceso incorrectas')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_dashborad(request):
    return render(request, 'user_dashboard.html')


@login_required
def home(request):
    """
    Renderiza la página principal de la aplicación.

    Esta vista requiere que el usuario haya iniciado sesión.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponse: Renderiza la plantilla 'home.html'.
    """
    # Si el usuario es un entrenador, lo redirige a su dashboard en trainer
    if request.user.role == 'trainer':
        return redirect('trainer:dashboard')
    return render(request, 'home.html', {'show_messages': True})

def logout_view(request):
    """
    Cierra la sesión del usuario actual.

    Después de cerrar sesión, redirige al usuario a la página principal.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponseRedirect: Redirige a la página principal ('home').
    """
    logout(request)
    # Eliminar mensajes de sesión
    storage = get_messages(request)
    for message in storage:
        pass  # Esto obliga a Django a marcar los mensajes como usados
    return redirect('home')

def crear_rutinas(request):
    """
    Maneja la creación de nuevas rutinas.

    Si la solicitud es POST, intenta guardar la rutina en la base de datos.
    Si es válida, redirige al usuario a la lista de rutinas.
    Si no es válida, renderiza nuevamente el formulario con errores.

    Args:
        request (HttpRequest): Objeto que representa la solicitud HTTP actual.

    Returns:
        HttpResponse: Renderiza la plantilla 'crear_rutina.html' con el formulario.
    """
    if request.method == 'POST':
        form = SimpleRutinaForm(request.POST)
        if form.is_valid():
            rutina = form.save()
            #pruebas con redirección home
            return redirect('home')
    else:
        form = SimpleRutinaForm()
    return render(request, 'crear_rutina.html', {'form': form})
