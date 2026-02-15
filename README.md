# School Canteen Management System

Автоматизированная информационная система школьного питания.

## Установка и развертывание

1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать окружение: `.\venv\Scripts\activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Выполнить миграции: `python manage.py migrate`
6. Заполнить базу тестовыми данными: `python fill_data.py`
7. Создать суперпользователя (админа): `python manage.py createsuperuser`
8. Запустить сервер: `python manage.py runserver`

## Видеоролик
Ссылка на видеоролик с демонстрацией: [https://rutube.ru/video/private/34b14fa202c8a742ad70def2ebdd0bd0/?p=150emStpxb80hIhaZD6zGw]
