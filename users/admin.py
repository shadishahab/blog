from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username','first_name', 'last_name', 'role', 'date_joined']
    list_display_links = ['id', 'username']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)