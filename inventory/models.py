from django.db import models
from menu.models import Dish


class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Килограмм'),
        ('g', 'Грамм'),
        ('l', 'Литр'),
        ('ml', 'Миллилитр'),
        ('pcs', 'Штук'),
    ]

    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    min_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.dish.name} - {self.ingredient.name}"


class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает согласования'),
        ('approved', 'Согласована'),
        ('rejected', 'Отклонена'),
        ('completed', 'Выполнена'),
    ]

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_requests')
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Заявка #{self.id} - {self.ingredient.name}"