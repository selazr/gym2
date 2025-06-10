from django.urls import path
from . import views

# namespace de la app
app_name = 'trainer'

# Rutas del trainer
urlpatterns = [
    path('listar/<str:tipo>/', views.multi_listados, name='multi_listados'),
    path('crear/rutina/', views.RoutineCreateUpdateView, name='crear_rutina'),
    path('editar/rutina/<int:pk>/', views.RoutineCreateUpdateView, name='editar_rutina'),
    path('ejercicios/crear/', views.ExerciseCreateView, name='crear_ejercicio'),
    path('ejercicios/editar/<str:pk>/', views.ExerciseUpdateView, name='editar_ejercicio'),
    path('eliminar/<str:tipo>/<str:pk>/', views.DeleteItemView, name='eliminar_item'),
    path('horario/', views.HorarioView, name='horario'),
    path('dashboard/', views.DashboardView, name='dashboard'),

]