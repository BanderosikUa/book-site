from django.contrib import admin
from .models import Author


class AuthorAdmin(admin.ModelAdmin):
    fields = ("name", "slug", "biography")
    prepopulated_fields = {"slug": ("name",)}


class AuthorAdminInline(admin.StackedInline):
    model = Author


admin.site.register(Author, AuthorAdmin)

# Register your models here.
