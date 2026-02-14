from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from .models import Order, Subscription, Payment
from menu.models import Dish


@login_required
def order_create(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)

    if request.method == 'POST':
        meal_date = request.POST.get('meal_date')
        quantity = int(request.POST.get('quantity', 1))
        use_subscription = request.POST.get('use_subscription')

        total_price = dish.price * quantity

        if use_subscription:
            subscriptions = Subscription.objects.filter(
                user=request.user,
                is_active=True,
                start_date__lte=meal_date,
                end_date__gte=meal_date
            )

            for subscription in subscriptions:
                if dish.meal_type == 'breakfast' and subscription.remaining_breakfast() >= quantity:
                    order = Order.objects.create(
                        user=request.user,
                        dish=dish,
                        meal_date=meal_date,
                        quantity=quantity,
                        price=0,
                        status='paid',
                        subscription=subscription
                    )
                    subscription.used_breakfast += quantity
                    subscription.save()
                    messages.success(request, 'Заказ создан по абонементу')
                    return redirect('order_history')
                elif dish.meal_type == 'lunch' and subscription.remaining_lunch() >= quantity:
                    order = Order.objects.create(
                        user=request.user,
                        dish=dish,
                        meal_date=meal_date,
                        quantity=quantity,
                        price=0,
                        status='paid',
                        subscription=subscription
                    )
                    subscription.used_lunch += quantity
                    subscription.save()
                    messages.success(request, 'Заказ создан по абонементу')
                    return redirect('order_history')

            messages.error(request, 'Нет подходящего абонемента с достаточным количеством приемов пищи')
            return redirect('order_create', dish_id=dish.id)

        if request.user.balance < total_price:
            messages.error(request, 'Недостаточно средств на балансе')
            return redirect('add_balance')

        order = Order.objects.create(
            user=request.user,
            dish=dish,
            meal_date=meal_date,
            quantity=quantity,
            price=total_price,
            status='paid'
        )

        request.user.balance -= total_price
        request.user.save()

        Payment.objects.create(
            user=request.user,
            order=order,
            amount=total_price,
            payment_type='single'
        )

        messages.success(request, 'Заказ успешно создан и оплачен')
        return redirect('order_history')

    active_subscriptions = Subscription.objects.filter(
        user=request.user,
        is_active=True,
        end_date__gte=timezone.now().date()
    )

    return render(request, 'orders/order_create.html', {
        'dish': dish,
        'today': timezone.now().date(),
        'subscriptions': active_subscriptions
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    subscriptions = Subscription.objects.filter(user=request.user, is_active=True)
    return render(request, 'orders/order_history.html', {
        'orders': orders,
        'subscriptions': subscriptions,
        'today': timezone.now().date()
    })


@login_required
def subscription_list(request):
    templates = Subscription.objects.filter(user__isnull=True)
    user_subscriptions = Subscription.objects.filter(user=request.user, is_active=True)
    return render(request, 'orders/subscription_list.html', {
        'subscriptions': templates,
        'user_subscriptions': user_subscriptions
    })


@login_required
def buy_subscription(request, subscription_id):
    template = get_object_or_404(Subscription, id=subscription_id, user__isnull=True)

    if request.method == 'POST':
        if request.user.balance < template.price:
            messages.error(request, 'Недостаточно средств на балансе')
            return redirect('add_balance')

        new_subscription = Subscription.objects.create(
            user=request.user,
            name=template.name,
            breakfast_count=template.breakfast_count,
            lunch_count=template.lunch_count,
            used_breakfast=0,
            used_lunch=0,
            price=template.price,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=30),
            is_active=True
        )

        request.user.balance -= template.price
        request.user.save()

        Payment.objects.create(
            user=request.user,
            subscription=new_subscription,
            amount=template.price,
            payment_type='subscription'
        )

        messages.success(request, 'Абонемент успешно приобретен')
        return redirect('order_history')

    return render(request, 'orders/buy_subscription.html', {'subscription': template})


@login_required
def mark_order_received(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'paid':
        order.status = 'completed'
        order.save()
        messages.success(request, 'Отметка о получении добавлена')
    else:
        messages.error(request, 'Заказ не оплачен')

    return redirect('order_history')


@login_required
def cook_dashboard(request):
    if request.user.role != 'cook':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    today = timezone.now().date()
    todays_orders = Order.objects.filter(meal_date=today).order_by('meal_date')
    completed_count = todays_orders.filter(status='completed').count()

    return render(request, 'orders/cook_dashboard.html', {
        'orders': todays_orders,
        'today': today,
        'completed_count': completed_count
    })


@login_required
def mark_order_served(request, order_id):
    if request.user.role != 'cook':
        messages.error(request, 'Доступ запрещен')
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)
    order.status = 'completed'
    order.save()

    messages.success(request, f'Заказ #{order.id} выдан')
    return redirect('cook_dashboard')


@login_required
def my_subscriptions(request):
    subscriptions = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-start_date')

    return render(request, 'orders/my_subscriptions.html', {
        'subscriptions': subscriptions,
        'today': timezone.now().date()
    })