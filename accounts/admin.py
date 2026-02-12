from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Allergy, Preference

admin.site.register(User, UserAdmin)
admin.site.register(Allergy)
admin.site.register(Preference)