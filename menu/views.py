from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DailyMenu, Dish

@login_required
def menu_list(request):
    today = timezone.now().date()
    menus = DailyMenu.objects.filter(date__gte=today).order_by('date')[:7]
    return render(request, 'menu/menu_list.html', {'menus': menus})

@login_required
def daily_menu(request, date):
    menu = DailyMenu.objects.get(date=date)
    return render(request, 'menu/daily_menu.html', {'menu': menu})