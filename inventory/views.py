from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models
from .models import Ingredient, PurchaseRequest


@login_required
def inventory_list(request):
    if request.user.role not in ['cook', 'admin']:
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    ingredients = Ingredient.objects.all().order_by('name')
    return render(request, 'inventory/inventory_list.html', {'ingredients': ingredients})


@login_required
def inventory_alerts(request):
    if request.user.role not in ['cook', 'admin']:
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    low_stock = Ingredient.objects.filter(quantity__lte=models.F('min_quantity'))
    return render(request, 'inventory/inventory_alerts.html', {'low_stock': low_stock})


@login_required
def purchase_request_list(request):
    if request.user.role == 'cook':
        requests = PurchaseRequest.objects.filter(created_by=request.user).order_by('-created_at')
    elif request.user.role == 'admin':
        requests = PurchaseRequest.objects.all().order_by('-created_at')
    else:
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    return render(request, 'inventory/purchase_request_list.html', {'requests': requests})


@login_required
def purchase_request_create(request):
    if request.user.role != 'cook':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient')
        quantity = request.POST.get('quantity')

        ingredient = get_object_or_404(Ingredient, id=ingredient_id)

        PurchaseRequest.objects.create(
            ingredient=ingredient,
            quantity=quantity,
            created_by=request.user,
            status='pending'
        )

        messages.success(request, 'Заявка на закупку создана')
        return redirect('purchase_request_list')

    ingredients = Ingredient.objects.all()
    return render(request, 'inventory/purchase_request_create.html', {'ingredients': ingredients})


@login_required
def purchase_request_approve(request, request_id):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    purchase_request = get_object_or_404(PurchaseRequest, id=request_id)
    purchase_request.status = 'approved'
    purchase_request.approved_by = request.user
    purchase_request.approved_at = timezone.now()
    purchase_request.save()

    ingredient = purchase_request.ingredient
    ingredient.quantity += purchase_request.quantity
    ingredient.save()

    messages.success(request, f'Заявка #{request_id} согласована')
    return redirect('purchase_request_list')


@login_required
def purchase_request_reject(request, request_id):
    if request.user.role != 'admin':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    purchase_request = get_object_or_404(PurchaseRequest, id=request_id)
    purchase_request.status = 'rejected'
    purchase_request.approved_by = request.user
    purchase_request.approved_at = timezone.now()
    purchase_request.save()

    messages.success(request, f'Заявка #{request_id} отклонена')
    return redirect('purchase_request_list')