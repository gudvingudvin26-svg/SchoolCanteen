from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import User, Allergy, Preference
from orders.models import Order, Payment
from inventory.models import PurchaseRequest
from reviews.models import Review


@login_required
def profile(request):
    if request.user.role == 'student':
        total_orders = Order.objects.filter(user=request.user).count()
        completed_orders = Order.objects.filter(user=request.user, status='completed').count()
        pending_orders = Order.objects.filter(user=request.user, status='paid').count()

        total_reviews = Review.objects.filter(user=request.user).count()
        recent_reviews = Review.objects.filter(user=request.user).order_by('-created_at')[:3]

        avg_rating = Review.objects.filter(user=request.user).aggregate(Avg('rating'))['rating__avg']

        context = {
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'total_reviews': total_reviews,
            'recent_reviews': recent_reviews,
            'avg_rating': avg_rating,
        }
        return render(request, 'accounts/profile.html', {'user': request.user, **context})

    return render(request, 'accounts/profile.html', {'user': request.user})


def home(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            context['total_payments'] = Order.objects.filter(status='paid').aggregate(Sum('price'))['price__sum'] or 0
            context['pending_requests'] = PurchaseRequest.objects.filter(status='pending').count()
    return render(request, 'accounts/home.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        role = request.POST.get('role', 'student')
        class_number = request.POST.get('class_number', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            class_number=class_number
        )
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('home')
    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверные учетные данные')
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def update_allergies(request):
    if request.method == 'POST':
        Allergy.objects.filter(user=request.user).delete()
        allergies = request.POST.getlist('allergies')
        for allergy in allergies:
            if allergy:
                Allergy.objects.create(user=request.user, name=allergy)
        messages.success(request, 'Аллергены обновлены')
    return redirect('profile')


@login_required
def update_preferences(request):
    if request.method == 'POST':
        Preference.objects.filter(user=request.user).delete()
        preferences = request.POST.getlist('preferences')
        for pref in preferences:
            if pref:
                Preference.objects.create(user=request.user, name=pref)
        messages.success(request, 'Предпочтения обновлены')
    return redirect('profile')


@login_required
def add_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', '').strip()

        if not amount:
            messages.error(request, 'Введите сумму')
            return redirect('profile')

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Сумма должна быть больше 0')
            elif amount > 100000:
                messages.error(request, 'Сумма не может превышать 100000 ₽')
            else:
                request.user.balance = float(request.user.balance) + amount
                request.user.save()
                messages.success(request, f'Баланс успешно пополнен на {amount} ₽')
        except ValueError:
            messages.error(request, 'Введите корректное число')

    return redirect('profile')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    date_to = timezone.now().date()
    date_from = date_to - timedelta(days=30)

    total_payments = Payment.objects.filter(
        payment_date__date__gte=date_from,
        payment_date__date__lte=date_to
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_orders = Order.objects.filter(
        status='completed',
        meal_date__gte=date_from,
        meal_date__lte=date_to
    ).count()

    pending_requests = PurchaseRequest.objects.filter(status='pending').count()

    payments_count = Payment.objects.filter(
        payment_date__date__gte=date_from,
        payment_date__date__lte=date_to
    ).count()

    subscriptions_count = Payment.objects.filter(
        payment_type='subscription',
        payment_date__date__gte=date_from,
        payment_date__date__lte=date_to
    ).count()

    single_payments_count = Payment.objects.filter(
        payment_type='single',
        payment_date__date__gte=date_from,
        payment_date__date__lte=date_to
    ).count()

    context = {
        'total_payments': total_payments,
        'total_orders': total_orders,
        'pending_requests': pending_requests,
        'payments_count': payments_count,
        'subscriptions_count': subscriptions_count,
        'single_payments_count': single_payments_count,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'admin_dashboard.html', context)