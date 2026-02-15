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
        use_subscription = request.POST.get('use_subscription') == 'on'

        price = dish.price * quantity
        final_price = 0 if use_subscription else price

        order = Order.objects.create(
            user=request.user,
            dish=dish,
            meal_date=meal_date,
            quantity=quantity,
            price=price,
            final_price=final_price,
            status='pending',
            used_subscription=use_subscription
        )

        if use_subscription:
            return redirect('pay_with_subscription', order_id=order.id)
        else:
            return redirect('order_payment', order_id=order.id)

    today = timezone.now().date()
    subscriptions = Subscription.objects.filter(
        user=request.user,
        is_active=True,
        end_date__gte=today
    )

    can_use_subscription = False
    for sub in subscriptions:
        if dish.meal_type == 'breakfast' and sub.breakfast_count > 0:
            can_use_subscription = True
            break
        elif dish.meal_type == 'lunch' and sub.lunch_count > 0:
            can_use_subscription = True
            break

    return render(request, 'orders/order_create.html', {
        'dish': dish,
        'today': today,
        'subscriptions': subscriptions,
        'can_use_subscription': can_use_subscription
    })


@login_required
def pay_with_subscription(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        subscription_id = request.POST.get('subscription_id')

        if not subscription_id:
            messages.error(request, 'Выберите абонемент')
            return redirect('pay_with_subscription', order_id=order.id)

        try:
            subscription = Subscription.objects.get(
                id=subscription_id,
                user=request.user,
                is_active=True
            )
        except Subscription.DoesNotExist:
            messages.error(request, 'Абонемент не найден или неактивен')
            return redirect('pay_with_subscription', order_id=order.id)

        if subscription.end_date < timezone.now().date():
            messages.error(request, 'Срок действия абонемента истек')
            return redirect('pay_with_subscription', order_id=order.id)

        if order.dish.meal_type == 'breakfast':
            if subscription.breakfast_count <= 0:
                messages.error(request, 'Недостаточно завтраков в абонементе')
                return redirect('pay_with_subscription', order_id=order.id)
            subscription.breakfast_count -= 1
        elif order.dish.meal_type == 'lunch':
            if subscription.lunch_count <= 0:
                messages.error(request, 'Недостаточно обедов в абонементе')
                return redirect('pay_with_subscription', order_id=order.id)
            subscription.lunch_count -= 1
        else:
            messages.error(request, 'Неизвестный тип приема пищи')
            return redirect('pay_with_subscription', order_id=order.id)

        subscription.save()

        order.status = 'paid'
        order.price = 0
        order.subscription = subscription
        order.save()

        messages.success(request, 'Заказ оплачен абонементом')
        return redirect('order_history')

    today = timezone.now().date()
    subscriptions = Subscription.objects.filter(
        user=request.user,
        is_active=True,
        end_date__gte=today
    )

    available_subs = []
    for sub in subscriptions:
        if order.dish.meal_type == 'breakfast' and sub.breakfast_count > 0:
            available_subs.append(sub)
        elif order.dish.meal_type == 'lunch' and sub.lunch_count > 0:
            available_subs.append(sub)

    if not available_subs:
        messages.warning(request, 'У вас нет подходящих абонементов для этого заказа')
        return redirect('order_create', dish_id=order.dish.id)

    return render(request, 'orders/pay_with_subscription.html', {
        'order': order,
        'subscriptions': available_subs
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


@login_required
def order_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        if request.user.balance >= order.price:
            request.user.balance -= order.price
            request.user.save()

            order.status = 'paid'
            order.save()

            messages.success(request, 'Заказ успешно оплачен')
            return redirect('order_history')
        else:
            messages.error(request, 'Недостаточно средств на балансе')
            return redirect('order_payment', order_id=order.id)

    return render(request, 'orders/order_payment.html', {'order': order})