from django.contrib import admin
from Authors.models import Author
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'genre', 'count_views', 'time_modified')
    search_fields = ('name', 'author')
    readonly_fields = ('time_modified', 'time_created')
    fields = ('name', 'slug', 'about', 'photo', 'author', 'genre',
              'time_created', 'time_modified')
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Book, BookAdmin)

# Register your models here.
