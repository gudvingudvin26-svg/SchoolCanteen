from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/allergies/', views.update_allergies, name='update_allergies'),
    path('profile/preferences/', views.update_preferences, name='update_preferences'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-balance/', views.add_balance, name='add_balance'),
]