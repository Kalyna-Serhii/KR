from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:turn_id>/', views.detail, name='detail'),
    path('<int:turn_id>/turn_register/', views.turn_register, name='turn_register'),
]
