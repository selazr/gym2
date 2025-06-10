from djongo import models
from django.conf import settings
from datetime import timedelta, date
from trainer.models import HorarioRutina


# Modelo para planes de suscripción
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    max_workouts_per_week = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.price}€/mes"

    class Meta:
        db_table = "subscription_plans"

# Modelo para la suscripción del usuario
class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, null=True, blank=True)  # Permitir que sea opcional
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)  # Permitir nulo para trainers

    def is_active(self):
        """Verifica si la suscripción sigue activa. Los trainers siempre están activos."""
        if self.user.role == "trainer":
            return True  # Trainers no necesitan suscripción
        return date.today() <= self.end_date

    def remaining_workouts(self):
        """Calcula los entrenamientos restantes según la suscripción actual. Trainers tienen rutinas ilimitadas."""
        if self.user.role == "trainer" or (self.plan and self.plan.max_workouts_per_week == -1):
            return float('inf')  # Rutinas ilimitadas para trainers

        start_of_week = date.today() - timedelta(days=date.today().weekday())  # Lunes de la semana actual
        workouts_this_week = UserWorkout.objects.filter(user=self.user, date__gte=start_of_week).count()
        return self.plan.max_workouts_per_week - workouts_this_week if self.plan else 0

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'Sin suscripción'}"

    class Meta:
        db_table = "user_subscriptions"

# Modelo para registrar entrenamientos del usuario
class UserWorkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(HorarioRutina, on_delete=models.CASCADE)
    date = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.rutinas_inscritas += 1
        self.user.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.user.rutinas_inscritas = max(0, self.user.rutinas_inscritas - 1)
        self.user.save()

    def __str__(self):
        return f"{self.user.username} - {self.session.rutina.nom} ({self.date})"

    class Meta:
        db_table = "user_workouts"
        unique_together = ["user", "session"]


