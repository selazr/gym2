from django.contrib.auth.models import AbstractUser
from djongo import models
from bson.objectid import ObjectId
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuari del Gimnàs'),
        ('trainer', 'Entrenador'),
        ('gerente', 'Gerente')
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    rutinas_inscritas = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 

class Rutina(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='routines'
    )
    ejercicios = models.ManyToManyField(
        'Exercise',
        related_name='routines',
        through='RoutineExercise'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RoutineExercise(models.Model):
    routine = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.IntegerField(default=0)
    sets = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.routine.name} - {self.exercise.name}"
