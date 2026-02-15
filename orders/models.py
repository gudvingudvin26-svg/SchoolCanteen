from django.db import models
from django.conf import settings
from menu.models import Dish


class OrderManager(models.Manager):
    def completed(self):
        return self.filter(status='completed')


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200)
    breakfast_count = models.IntegerField(default=0)
    lunch_count = models.IntegerField(default=0)
    used_breakfast = models.IntegerField(default=0)
    used_lunch = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.name}"
        return f"Шаблон: {self.name}"

    def remaining_breakfast(self):
        return self.breakfast_count - self.used_breakfast

    def remaining_lunch(self):
        return self.lunch_count - self.used_lunch

    def is_valid(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('completed', 'Получен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    meal_date = models.DateField()
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    used_subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ {self.id} - {self.user.username}"


class Payment(models.Model):
    PAYMENT_TYPE = [
        ('single', 'Разовый'),
        ('subscription', 'Абонемент'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)

    def __str__(self):
        return f"Платеж {self.id} - {self.amount} ₽"