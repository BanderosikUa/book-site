from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    model = User

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
    )w
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
