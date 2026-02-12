from django.contrib import admin
from .models import Category, Dish, DailyMenu

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(DailyMenu)