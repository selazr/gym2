from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan, UserSubscription, UserWorkout
from datetime import date, timedelta
from trainer.models import  HorarioRutina
from bson import ObjectId
from gym_app.models import User

# Subscripción del usuario a los diferentes planes
@login_required
def subscriptions_view(request):
    """ Muestra los planes de suscripción y permite elegir uno. """
    plans = SubscriptionPlan.objects.all()

    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)

        subscription, created = UserSubscription.objects.update_or_create(
            user=request.user,
            defaults={
                "plan": plan,
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=30),
            }
        )
        messages.success(request, f"Te has suscrito al plan {plan.name}")
        return redirect("gym_workouts:schedule")

    return render(request, "gym_workouts/subscriptions.html", {"plans": plans})

# Horario de rutinas en el que el usuario se puede unir
@login_required
def schedule_view(request):
    user = request.user
    subscription = UserSubscription.objects.filter(user=user).first()
    is_subscribed = subscription and subscription.is_active()

    if request.method == "POST":
        action = request.POST.get("action")
        session_id = request.POST.get("session_id")

        try:
            session = get_object_or_404(HorarioRutina, _id=ObjectId(session_id))
        except Exception:
            messages.error(request, "Sesión no encontrada.")
            return redirect("gym_workouts:schedule")

        user_id_str = str(user.id)

        # Asegurar que session.inscritos es una lista
        if not isinstance(session.inscritos, list):
            session.inscritos = []

        if action == "join":
            if not is_subscribed:
                messages.error(request, "Debes tener una suscripción activa para inscribirte.")
            elif len(session.inscritos) >= 10:
                messages.error(request, "No hay cupos disponibles en esta rutina.")
            elif user_id_str in session.inscritos:
                messages.error(request, "Ya estás inscrito en esta rutina.")
            else:
                session.inscritos.append(user_id_str)
                session.save()
                messages.success(request, "Te has inscrito correctamente.")

        elif action == "leave":
            if user_id_str in session.inscritos:
                session.inscritos.remove(user_id_str)
                session.save()
                messages.success(request, "Has cancelado tu inscripción correctamente.")
            else:
                messages.error(request, "No estás inscrito en esta rutina.")

        return redirect("gym_workouts:schedule")

    rutinas = HorarioRutina.objects.select_related("rutina").all()
    for rutina in rutinas:
        rutina.id_str = str(rutina._id)

    dias_traducidos = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes"
    }

    fechas_disponibles = []
    fecha_actual = date.today()

    for _ in range(5):
        while fecha_actual.weekday() >= 5:
            fecha_actual += timedelta(days=1)
        dia_nombre = dias_traducidos[fecha_actual.strftime('%A')]
        fechas_disponibles.append({"nombre": dia_nombre, "numero": fecha_actual.day, "fecha": fecha_actual})
        fecha_actual += timedelta(days=1)

    horas_disponibles = [16, 17, 18, 19, 20, 21]

    return render(request, "gym_workouts/schedule.html", {
        "rutinas": rutinas,
        "fechas_disponibles": fechas_disponibles,
        "horas_disponibles": horas_disponibles,
        "is_subscribed": is_subscribed
    })
