from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Ученик'),
        ('cook', 'Повар'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    class_number = models.CharField(max_length=10, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Allergy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='allergies')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name