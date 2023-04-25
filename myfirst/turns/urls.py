from turns.views import *
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', create_turn, name='create_turn'),
    path('<int:turn_id>/', views.detail, name='detail'),
    path('<int:turn_id>/open/', views.open_turn, name='open_turn'),
    path('<int:turn_id>/close/', views.close_turn, name='close_turn'),
    path('<int:turn_id>/delete/', delete_turn, name='delete_turn'),
    path('<int:turn_id>/register/', turn_register, name='turn_register'),
    path('<int:turn_id>/unregister/', turn_unregister, name='turn_unregister'),
    path('<int:turn_id>/next_turn_user/', next_turn_user, name='next_turn_user'),
    path('<int:turn_id>/delete_turn_user/', delete_turn_user, name='delete_turn_user'),
]
