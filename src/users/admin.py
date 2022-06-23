from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'email',
                    'avatar',
                    'groups',
                )
            }
        )
    )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
