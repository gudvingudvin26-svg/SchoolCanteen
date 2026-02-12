from django.urls import path
from . import views

urlpatterns = [
    path('dish/<int:dish_id>/', views.review_list, name='review_list'),
    path('create/<int:dish_id>/', views.review_create, name='review_create'),
]