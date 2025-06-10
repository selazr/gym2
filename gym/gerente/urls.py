from django.urls import path
from .views import user_list_view

app_name = 'gerente'

urlpatterns = [
    path('users/', user_list_view, name='user_list'),
]
