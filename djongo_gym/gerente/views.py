from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def is_gerent(user):
    """Función para verificar si el usuario es gerente"""
    return user.is_authenticated and user.role == 'gerente'

@login_required
@user_passes_test(is_gerent)
def user_list_view(request):
    """Vista para que el gerente pueda visualizar, buscar y ordenar usuarios"""

    search_query = request.GET.get('search', '')  # Captura la búsqueda
    order_by = request.GET.get('order_by', 'username')  # Captura el criterio de ordenación
    page_number = request.GET.get('page', 1)  # Captura la página actual

    # Filtrar usuarios si hay un término de búsqueda
    users = User.objects.all()
    if search_query:
        users = users.filter(username__icontains=search_query) | \
                users.filter(email__icontains=search_query) | \
                users.filter(first_name__icontains=search_query) | \
                users.filter(last_name__icontains=search_query)

    # Ordenar los resultados
    users = users.order_by(order_by)

    # Paginación
    paginator = Paginator(users, 10)  # 10 usuarios por página
    users_page = paginator.get_page(page_number)

    return render(request, 'gerente/user_list.html', {
        'users': users_page,
        'search_query': search_query,
        'order_by': order_by
    })
