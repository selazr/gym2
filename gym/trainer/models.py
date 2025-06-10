from django.contrib.auth.models import AbstractUser
from djongo import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from bson import ObjectId
from datetime import date, timedelta


# class SessioRutina(models.Model):
#     rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
#     data = models.DateField()
#     hora_inici = models.TimeField()
#     hora_fi = models.TimeField()
#     sala = models.CharField(max_length=100)
#     participants = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='sessions_inscrites',
#         limit_choices_to={'role': 'user'},
#         blank=True
#     )

#     class Meta:
#         db_table = 'sessions_rutina'
#         unique_together = ['sala', 'data', 'hora_inici']

class TrainerExercise(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'trainer_exercise'
    
class TrainerRutina(models.Model):
    nom = models.CharField(max_length=100)
    descripcio = models.TextField()
    exercises = models.ManyToManyField(TrainerExercise, related_name='rutinas')
    dificultat = models.CharField(
        max_length=10,
        choices=[
            ('Fácil', 'Fácil'),
            ('Intermedio', 'Intermedio'),
            ('Difícil', 'Difícil')
        ],
        default='Fácil'
    )
    energia = models.IntegerField(
        choices=[
            (3, 'Bajo'),
            (7, 'Medio'),
            (10, 'Alto')
        ],
        default=7
    )

    class Meta:
        db_table = 'rutines'

class HorarioRutina(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    rutina = models.ForeignKey("TrainerRutina", on_delete=models.CASCADE)
    dia = models.CharField(
        max_length=10,
        choices=[
            ('Lunes', 'Lunes'),
            ('Martes', 'Martes'),
            ('Miércoles', 'Miércoles'),
            ('Jueves', 'Jueves'),
            ('Viernes', 'Viernes')
        ]
    )
    dia_numero = models.IntegerField()
    hora = models.IntegerField(choices=[
        (16, "16:00"), (17, "17:00"), (18, "18:00"), 
        (19, "19:00"), (20, "20:00"), (21, "21:00")
    ])
    inscritos = models.JSONField(default=list)  # Asegurar que es una lista

    def save(self, *args, **kwargs):
        """Asegurar que inscritos es una lista antes de guardar"""
        if not isinstance(self.inscritos, list):
            self.inscritos = []  # Reiniciar como lista si no lo es
        super().save(*args, **kwargs)

    def inscribir_usuario(self, user_id):
        """Añade un usuario a la lista de inscritos si no está ya inscrito."""
        user_id_str = str(user_id)
        if user_id_str not in self.inscritos and len(self.inscritos) < 10:
            self.inscritos.append(user_id_str)
            self.save()

    def cancelar_inscripcion(self, user_id):
        """Elimina un usuario de la lista de inscritos."""
        user_id_str = str(user_id)
        if user_id_str in self.inscritos:
            self.inscritos.remove(user_id_str)
            self.save()

    class Meta:
        unique_together = ['dia', 'hora', 'dia_numero']
        db_table = 'trainer_horariorutina'