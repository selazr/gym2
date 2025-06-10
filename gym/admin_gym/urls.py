from django.urls import path
from .views import user_list, create_user, update_user, delete_user

app_name = 'admin'

urlpatterns = [
    path('users/', user_list, name='user_list'),
    path('users/create/', create_user, name='create_user'),
    path('users/update/<int:user_id>/', update_user, name='update_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
]
