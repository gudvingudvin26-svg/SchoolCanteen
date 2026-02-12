from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Dish(models.Model):
    MEAL_TYPE = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE)
    calories = models.IntegerField(default=0)
    proteins = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    allergens = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='dishes/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DailyMenu(models.Model):
    date = models.DateField()
    breakfast_items = models.ManyToManyField(Dish, related_name='breakfast_menus',
                                             limit_choices_to={'meal_type': 'breakfast'})
    lunch_items = models.ManyToManyField(Dish, related_name='lunch_menus', limit_choices_to={'meal_type': 'lunch'})

    class Meta:
        unique_together = ['date']

    def __str__(self):
        return f"Меню на {self.date}"