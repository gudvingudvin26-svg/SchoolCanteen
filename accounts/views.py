from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Allergy, Preference


def home(request):
    return render(request, 'accounts/home.html')


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

        try:
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
            return redirect('home')
        except:
            messages.error(request, 'Ошибка при регистрации')
            return render(request, 'accounts/register.html')

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
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


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


from decimal import Decimal

@login_required
def add_balance(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', 0))
        request.user.balance += amount
        request.user.save()
        messages.success(request, f'Баланс пополнен на {amount} ₽')
        return redirect('profile')
    return render(request, 'accounts/add_balance.html')