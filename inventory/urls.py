from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('alerts/', views.inventory_alerts, name='inventory_alerts'),
    path('purchase/requests/', views.purchase_request_list, name='purchase_request_list'),
    path('purchase/create/', views.purchase_request_create, name='purchase_request_create'),
    path('purchase/approve/<int:request_id>/', views.purchase_request_approve, name='purchase_request_approve'),
    path('purchase/reject/<int:request_id>/', views.purchase_request_reject, name='purchase_request_reject'),
]