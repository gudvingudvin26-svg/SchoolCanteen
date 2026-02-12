from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_dashboard, name='reports_dashboard'),
    path('finance/', views.finance_report, name='finance_report'),
    path('attendance/', views.attendance_report, name='attendance_report'),
    path('inventory/', views.inventory_report, name='inventory_report'),
]