from django.db import models
from django.conf import settings
from orders.models import Order, Payment
from inventory.models import PurchaseRequest


class Report(models.Model):
    REPORT_TYPES = [
        ('finance', 'Финансовый отчет'),
        ('attendance', 'Отчет по посещаемости'),
        ('inventory', 'Отчет по складу'),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date_from = models.DateField()
    date_to = models.DateField()
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.title} - {self.created_at.date()}"