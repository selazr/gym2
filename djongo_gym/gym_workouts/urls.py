from django.urls import path
from . import views

app_name = "gym_workouts"

urlpatterns = [
    path('subscriptions/', views.subscriptions_view, name='subscriptions'),
    path("schedule/", views.schedule_view, name="schedule"),

]