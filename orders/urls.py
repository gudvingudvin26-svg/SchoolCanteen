from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:dish_id>/', views.order_create, name='order_create'),
    path('history/', views.order_history, name='order_history'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('my-subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    path('subscription/buy/<int:subscription_id>/', views.buy_subscription, name='buy_subscription'),
    path('mark_received/<int:order_id>/', views.mark_order_received, name='mark_order_received'),
    path('cook/dashboard/', views.cook_dashboard, name='cook_dashboard'),
    path('cook/mark_served/<int:order_id>/', views.mark_order_served, name='mark_order_served'),
]