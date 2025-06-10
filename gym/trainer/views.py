from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from trainer.forms import RoutineForm, ExerciseForm
from .models import TrainerRutina, TrainerExercise, HorarioRutina
from bson import ObjectId
import hashlib
from datetime import date, timedelta
import traceback  # Importar para capturar el detalle del error


# Vista para listar ejercicios o rutinas
@login_required
def multi_listados(request, tipo):
    if tipo == 'ejercicios':
        items = TrainerExercise.objects.all()
        crear_url = 'trainer:crear_ejercicio'
    elif tipo == 'rutinas':
        items = TrainerRutina.objects.all()
        crear_url = 'trainer:crear_rutina'
    else:
        messages.error(request, 'Vista no válida')
        return redirect('trainer:multi_listados', tipo='ejercicios')

    return render(request, 'trainer/multi_listados.html', {
        'items': items,
        'tipo': tipo,
        'crear_url': crear_url
    })

# Vista para crear una nueva rutina
@login_required
def RoutineCreateView(request):
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Rutina creada exitosamente')
                return redirect('trainer:multi_listados', tipo='rutinas')
            except Exception as e:
                messages.error(request, f'Error al crear la rutina: {str(e)}')
    else:
        form = RoutineForm()

    return render(request, 'trainer/crear_rutina.html', {
        'form': form
    })

# Vista para crear o actualizar una rutina
@login_required
def RoutineCreateUpdateView(request, pk=None):
    ejercicios = TrainerExercise.objects.all()
    # Si se proporciona un ID, se obtiene la rutina existente
    if pk:
        rutina = get_object_or_404(TrainerRutina, pk=pk)
    else:
        rutina = None

    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=rutina)
        if form.is_valid():
            rutina = form.save()
            rutina.exercises.set(request.POST.getlist('ejercicios'))  # Asociar ejercicios seleccionados
            rutina.save()

            if pk:
                messages.success(request, 'Rutina actualizada exitosamente')
            else:
                messages.success(request, 'Rutina creada exitosamente')
            return redirect('trainer:multi_listados', tipo='rutinas')
    else:
        form = RoutineForm(instance=rutina)

    return render(request, 'trainer/crear_rutina.html', {
        'form': form,
        'ejercicios': ejercicios,
        'edit_mode': bool(pk)
    })


# Vista para crear un ejercicio
@login_required
def ExerciseCreateView(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Ejercicio creado exitosamente')
                return redirect('trainer:multi_listados', tipo='ejercicios')
            except Exception as e:
                print(f'Error al crear el ejercicio: {e}')
                traceback.print_exc()  # Esto imprimirá el detalle completo del error en la consola
                messages.error(request, f'Error al crear el ejercicio: {str(e)}')
        else:
            print(f'Errores de validación del formulario: {form.errors}')
            messages.error(request, 'El formulario no es válido')
    else:
        form = ExerciseForm()

    return render(request, 'trainer/crear_ejercicio.html', {'form': form})


# Vista para actualizar un ejercicio existente
@login_required
def ExerciseUpdateView(request, pk):
    ejercicio = get_object_or_404(TrainerExercise, id=ObjectId(pk))
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=ejercicio)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Ejercicio actualizado exitosamente')
                return redirect('trainer:multi_listados', tipo='ejercicios')
            except Exception as e:
                messages.error(request, f'Error al actualizar el ejercicio: {str(e)}')
    else:
        form = ExerciseForm(instance=ejercicio)

    return render(request, 'trainer/crear_ejercicio.html', {'form': form, 'edit_mode': True})

# Vista para gestionar horarios de rutinas
@login_required
def RoutineCreateUpdateView(request, pk=None):
    ejercicios = TrainerExercise.objects.all()

    if pk:
        try:
            rutina = get_object_or_404(TrainerRutina, id=int(pk))
            edit_mode = True
        except Exception:
            messages.error(request, "Rutina no encontrada.")
            return redirect('trainer:multi_listados', tipo='rutinas')
    else:
        rutina = None
        edit_mode = False

    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=rutina)
        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.save()

            # Asociar los ejercicios seleccionados
            ejercicios_ids = request.POST.getlist('exercises')
            rutina.exercises.set(ejercicios_ids)
            rutina.save()

            if edit_mode:
                messages.success(request, 'Rutina actualizada exitosamente')
            else:
                messages.success(request, 'Rutina creada exitosamente')

            return redirect('trainer:multi_listados', tipo='rutinas')
        else:
            print(f'Errores en el formulario: {form.errors}')
            messages.error(request, 'El formulario no es válido')
    else:
        form = RoutineForm(instance=rutina)

    return render(request, 'trainer/crear_rutina.html', {
        'form': form,
        'ejercicios': ejercicios,
        'edit_mode': edit_mode,
        'rutina': rutina
    })

# Vista para eliminar ejercicios o rutinas
@login_required
def DeleteItemView(request, tipo, pk):
    if tipo == 'ejercicio':
        item = get_object_or_404(TrainerExercise, id=ObjectId(pk))
    elif tipo == 'rutina':
        item = get_object_or_404(TrainerRutina, id=ObjectId(pk))
        # Eliminar solo las instancias de HorarioRutina asociadas a esta rutina considerando día y hora
        HorarioRutina.objects.filter(rutina=item).delete()
    else:
        messages.error(request, 'Tipo de elemento no válido')
        return redirect('trainer:multi_listados', tipo='ejercicios')

    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, f'{tipo.capitalize()} eliminado exitosamente')
            return redirect('trainer:multi_listados', tipo=tipo + 's')
        except Exception as e:
            messages.error(request, f'Error al eliminar el {tipo}: {str(e)}')

    return render(request, 'trainer/eliminar_item.html', {
        'item': item,
        'tipo': tipo
    })

# Vista para gestionar horarios de rutinas
@login_required
def HorarioView(request):
    rutinas = TrainerRutina.objects.all()
    horario = HorarioRutina.objects.all()

    # Mapeo de días en inglés a español
    dias_traducidos = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes"
    }

    # Obtener la fecha actual y avanzar si es fin de semana
    fecha_actual = date.today()
    while fecha_actual.weekday() > 4:  # Si es sábado (5) o domingo (6), avanzar al lunes
        fecha_actual += timedelta(days=1)

    # Crear lista de fechas disponibles
    fechas_disponibles = []
    for _ in range(5):  # Mostrar solo 5 días hábiles
        while fecha_actual.weekday() > 4:  # Saltar sábados y domingos
            fecha_actual += timedelta(days=1)
        dia_espanol = dias_traducidos[fecha_actual.strftime('%A')]  # Traducir el día
        fechas_disponibles.append((dia_espanol, fecha_actual.day))
        fecha_actual += timedelta(days=1)

    # Diccionario de colores basado en la rutina
    rutina_colores = {
        str(rutina.id): f"#{hashlib.md5(str(rutina.id).encode()).hexdigest()[:6]}"
        for rutina in rutinas
    }

    # Construcción de la lista de horarios
    horario_lista = []
    for dia_nombre, dia_num in fechas_disponibles:
        for hora in range(16, 22):
            entry = horario.filter(dia=dia_nombre, dia_numero=dia_num, hora=hora).first()
            horario_lista.append({
                "dia": dia_nombre,
                "dia_numero": dia_num,
                "hora": hora,
                "entry": entry,
                "rutina_color": rutina_colores.get(str(entry.rutina.id), "#cccccc") if entry else "#f8f9fa"
            })

    # Manejar la asignación o eliminación de rutinas
    if request.method == "POST":
        dia = request.POST.get("dia")
        dia_numero = int(request.POST.get("dia_numero"))
        hora = int(request.POST.get("hora"))
        rutina_id = request.POST.get("rutina_id")

        if not rutina_id:
            HorarioRutina.objects.filter(dia=dia, dia_numero=dia_numero, hora=hora).delete()
            messages.success(request, "Rutina eliminada.")
        else:
            rutina = get_object_or_404(TrainerRutina, id=int(rutina_id))
            HorarioRutina.objects.update_or_create(
                dia=dia, dia_numero=dia_numero, hora=hora, defaults={"rutina": rutina}
            )
            messages.success(request, "Rutina programada correctamente.")

        return redirect("trainer:horario")

    return render(request, "trainer/horario.html", {
        "horario_lista": horario_lista,
        "dias_disponibles": fechas_disponibles,
        "rutinas": rutinas
    })

# Vista para el panel de control
@login_required
def DashboardView(request):
    if request.method != 'GET':  # Asegura que solo acepte GET
        return render(request, '403.html', status=403)

    rutinas = TrainerRutina.objects.all()
    horario = HorarioRutina.objects.all()

    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

    rutina_colores = {
        str(rutina.id): f"#{hashlib.md5(str(rutina.id).encode()).hexdigest()[:6]}"
        for rutina in rutinas
    }

    horario_lista = []
    for dia in dias_semana:
        for hora in range(16, 22):
            entry = horario.filter(dia=dia, hora=hora).first()
            horario_lista.append({
                "dia": dia,
                "hora": hora,
                "entry": entry,
                "rutina_color": rutina_colores.get(str(entry.rutina.id), "#cccccc") if entry else "#f8f9fa"
            })

    return render(request, "trainer/dashboard.html", {
        "horario_lista": horario_lista,
        "dias_semana": dias_semana
    })