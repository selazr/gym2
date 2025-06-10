from django.contrib import admin
from gym_app.models import User, Rutina, Exercise, RoutineExercise

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'created_at')
    search_fields = ('name', 'trainer__username')
    list_filter = ('created_at',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(RoutineExercise)
class RoutineExerciseAdmin(admin.ModelAdmin):
    list_display = ('routine', 'exercise', 'repetitions', 'sets')
    list_filter = ('routine', 'exercise')

