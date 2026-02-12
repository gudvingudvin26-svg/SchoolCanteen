import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_project.settings')
django.setup()

from accounts.models import User
from menu.models import Category, Dish, DailyMenu
from inventory.models import Ingredient
from orders.models import Subscription

print('Удаляем старые меню...')
DailyMenu.objects.all().delete()
print('  Все меню удалены')

print('\nСоздаем пользователей...')

cook, _ = User.objects.get_or_create(
    username='cook',
    defaults={
        'first_name': 'Анна',
        'last_name': 'Иванова',
        'email': 'cook@school.ru',
        'role': 'cook',
        'is_staff': True
    }
)
if _:
    cook.set_password('cook123')
    cook.save()
    print('  Повар создан')

student, _ = User.objects.get_or_create(
    username='student',
    defaults={
        'first_name': 'Иван',
        'last_name': 'Петров',
        'email': 'student@school.ru',
        'role': 'student',
        'class_number': '7А',
        'balance': 2000
    }
)
if _:
    student.set_password('student123')
    student.save()
    print('  Ученик создан')

print('\nСоздаем категории...')
breakfast_cat, _ = Category.objects.get_or_create(name='Завтраки')
lunch_cat, _ = Category.objects.get_or_create(name='Обеды')
soup_cat, _ = Category.objects.get_or_create(name='Супы')
main_cat, _ = Category.objects.get_or_create(name='Горячие блюда')
salad_cat, _ = Category.objects.get_or_create(name='Салаты')
drink_cat, _ = Category.objects.get_or_create(name='Напитки')
print('  Категории созданы')

print('\nСоздаем продукты на складе...')
ingredients_data = [
    {'name': 'Молоко', 'unit': 'l', 'quantity': 50, 'min_quantity': 10, 'price_per_unit': 60},
    {'name': 'Яйца', 'unit': 'pcs', 'quantity': 200, 'min_quantity': 50, 'price_per_unit': 8},
    {'name': 'Мука', 'unit': 'kg', 'quantity': 30, 'min_quantity': 5, 'price_per_unit': 45},
    {'name': 'Курица', 'unit': 'kg', 'quantity': 25, 'min_quantity': 5, 'price_per_unit': 200},
    {'name': 'Картофель', 'unit': 'kg', 'quantity': 80, 'min_quantity': 20, 'price_per_unit': 30},
    {'name': 'Морковь', 'unit': 'kg', 'quantity': 15, 'min_quantity': 5, 'price_per_unit': 25},
    {'name': 'Лук', 'unit': 'kg', 'quantity': 12, 'min_quantity': 3, 'price_per_unit': 20},
    {'name': 'Гречка', 'unit': 'kg', 'quantity': 20, 'min_quantity': 5, 'price_per_unit': 50},
    {'name': 'Рис', 'unit': 'kg', 'quantity': 20, 'min_quantity': 5, 'price_per_unit': 55},
    {'name': 'Масло подсолнечное', 'unit': 'l', 'quantity': 15, 'min_quantity': 3, 'price_per_unit': 100},
]

for data in ingredients_data:
    ing, created = Ingredient.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    if created:
        print(f'  + {data["name"]}')


print('\nСоздаем блюда...')

dishes_data = [
    {
        'name': 'Каша овсяная с фруктами',
        'category': breakfast_cat,
        'description': 'Овсяная каша на молоке с яблоком и бананом',
        'price': 120,
        'meal_type': 'breakfast',
        'calories': 320,
        'proteins': 8.5,
        'fats': 6.2,
        'carbohydrates': 45,
        'allergens': 'Глютен, Лактоза'
    },
    {
        'name': 'Сырники со сметаной',
        'category': breakfast_cat,
        'description': 'Творожные сырники, подаются со сметаной',
        'price': 150,
        'meal_type': 'breakfast',
        'calories': 380,
        'proteins': 15,
        'fats': 12,
        'carbohydrates': 35,
        'allergens': 'Глютен, Лактоза, Яйца'
    },
    {
        'name': 'Омлет с сыром',
        'category': breakfast_cat,
        'description': 'Пышный омлет из двух яиц с сыром',
        'price': 130,
        'meal_type': 'breakfast',
        'calories': 290,
        'proteins': 14,
        'fats': 18,
        'carbohydrates': 4,
        'allergens': 'Лактоза, Яйца'
    },
    {
        'name': 'Борщ со сметаной',
        'category': soup_cat,
        'description': 'Классический борщ с говядиной',
        'price': 180,
        'meal_type': 'lunch',
        'calories': 210,
        'proteins': 12,
        'fats': 8,
        'carbohydrates': 20,
        'allergens': ''
    },
    {
        'name': 'Котлета куриная с пюре',
        'category': main_cat,
        'description': 'Куриная котлета и картофельное пюре',
        'price': 200,
        'meal_type': 'lunch',
        'calories': 450,
        'proteins': 25,
        'fats': 15,
        'carbohydrates': 40,
        'allergens': ''
    },
    {
        'name': 'Макароны по-флотски',
        'category': main_cat,
        'description': 'Макароны с мясным фаршем',
        'price': 170,
        'meal_type': 'lunch',
        'calories': 420,
        'proteins': 18,
        'fats': 16,
        'carbohydrates': 50,
        'allergens': 'Глютен'
    },
    {
        'name': 'Салат из свежих овощей',
        'category': salad_cat,
        'description': 'Огурцы, помидоры, перец, зелень',
        'price': 90,
        'meal_type': 'lunch',
        'calories': 80,
        'proteins': 2,
        'fats': 4,
        'carbohydrates': 10,
        'allergens': ''
    },
    {
        'name': 'Компот из сухофруктов',
        'category': drink_cat,
        'description': 'Натуральный компот',
        'price': 50,
        'meal_type': 'lunch',
        'calories': 90,
        'proteins': 0,
        'fats': 0,
        'carbohydrates': 22,
        'allergens': ''
    },
]

for dish_data in dishes_data:
    dish, created = Dish.objects.get_or_create(
        name=dish_data['name'],
        defaults=dish_data
    )
    if created:
        print(f'  + {dish_data["name"]}')

print('\nСоздаем меню на будние дни...')

breakfasts = Dish.objects.filter(meal_type='breakfast')[:3]
lunches = Dish.objects.filter(meal_type='lunch')[:5]

today = date.today()
days_added = 0
current_date = today

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

while days_added < 5:

    if current_date.weekday() < 5:  # Только Пн-Пт
        daily_menu = DailyMenu.objects.create(date=current_date)
        daily_menu.breakfast_items.set(breakfasts)
        daily_menu.lunch_items.set(lunches[:3])
        daily_menu.save()
        print(f'  + {current_date} ({weekdays[current_date.weekday()]})')
        days_added += 1
    current_date += timedelta(days=1)

print('\nСоздаем абонементы...')

subscriptions_data = [
    {
        'name': 'Завтрак на месяц',
        'breakfast_count': 20,
        'lunch_count': 0,
        'price': 2000
    },
    {
        'name': 'Обед на месяц',
        'breakfast_count': 0,
        'lunch_count': 20,
        'price': 3000
    },
    {
        'name': 'Полный день',
        'breakfast_count': 20,
        'lunch_count': 20,
        'price': 4500
    },
]

for sub_data in subscriptions_data:
    existing = Subscription.objects.filter(
        name=sub_data['name'],
        user__isnull=True
    ).first()

    if not existing:
        sub = Subscription.objects.create(
            user=None,
            name=sub_data['name'],
            breakfast_count=sub_data['breakfast_count'],
            lunch_count=sub_data['lunch_count'],
            price=sub_data['price'],
            start_date=today,
            end_date=today + timedelta(days=30),
            is_active=True
        )
        print(f'  + {sub_data["name"]} - {sub_data["price"]}₽')
    else:
        print(f'  • {sub_data["name"]} уже существует')

print('\n' + '=' * 50)
print('ГОТОВО! Система готова к работе!')
print('=' * 50)
print('\nУчетные данные:')
print('  Админ:   admin / admin123 (создайте через createsuperuser)')
print('  Повар:   cook / cook123')
print('  Ученик:  student / student123')
print('\nМеню создано только на будние дни:')
for menu in DailyMenu.objects.all().order_by('date'):
    print(f'  - {menu.date} ({weekdays[menu.date.weekday()]})')
print('\nСсылки:')
print('  Сайт:        http://127.0.0.1:8000')
print('  Админка:     http://127.0.0.1:8000/admin')