from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from orders.models import Order, Payment
from accounts.models import User
from inventory.models import PurchaseRequest
from datetime import timedelta


@login_required
def reports_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    return render(request, 'reports/reports_dashboard.html')


@login_required
def finance_report(request):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    date_to = timezone.now().date()
    date_from = date_to - timedelta(days=30)

    payments = Payment.objects.filter(payment_date__date__gte=date_from, payment_date__date__lte=date_to)
    total_revenue = payments.aggregate(Sum('amount'))['amount__sum'] or 0

    purchases = PurchaseRequest.objects.filter(created_at__date__gte=date_from, created_at__date__lte=date_to,
                                               status='approved')
    total_expenses = 0
    for purchase in purchases:
        total_expenses += float(purchase.quantity) * float(purchase.ingredient.price_per_unit)

    context = {
        'date_from': date_from,
        'date_to': date_to,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'payments': payments[:50],
    }

    return render(request, 'reports/finance_report.html', context)


@login_required
def attendance_report(request):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    date_to = timezone.now().date()
    date_from = date_to - timedelta(days=30)

    completed_orders = Order.objects.filter(
        status='completed',
        meal_date__gte=date_from,
        meal_date__lte=date_to
    )

    daily_stats = []
    current_date = date_from
    while current_date <= date_to:
        daily_orders = completed_orders.filter(meal_date=current_date)
        daily_stats.append({
            'date': current_date,
            'breakfast_count': daily_orders.filter(dish__meal_type='breakfast').count(),
            'lunch_count': daily_orders.filter(dish__meal_type='lunch').count(),
            'total': daily_orders.count()
        })
        current_date += timedelta(days=1)

    context = {
        'date_from': date_from,
        'date_to': date_to,
        'daily_stats': daily_stats,
        'total_orders': completed_orders.count(),
    }

    return render(request, 'reports/attendance_report.html', context)


@login_required
def inventory_report(request):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    from inventory.models import Ingredient

    ingredients = Ingredient.objects.all()
    purchase_requests = PurchaseRequest.objects.filter(status='approved').order_by('-approved_at')[:50]

    context = {
        'ingredients': ingredients,
        'purchase_requests': purchase_requests,
    }

    return render(request, 'reports/inventory_report.html', context)