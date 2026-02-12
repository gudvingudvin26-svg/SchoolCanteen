from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('daily/<str:date>/', views.daily_menu, name='daily_menu'),
]