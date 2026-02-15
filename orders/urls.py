from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:dish_id>/', views.order_create, name='order_create'),
    path('payment/<int:order_id>/', views.order_payment, name='order_payment'),
    path('history/', views.order_history, name='order_history'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('subscription/buy/<int:subscription_id>/', views.buy_subscription, name='buy_subscription'),
    path('mark_received/<int:order_id>/', views.mark_order_received, name='mark_order_received'),
    path('cook/dashboard/', views.cook_dashboard, name='cook_dashboard'),
    path('cook/mark_served/<int:order_id>/', views.mark_order_served, name='mark_order_served'),
    path('pay-with-subscription/<int:order_id>/', views.pay_with_subscription, name='pay_with_subscription'),
]