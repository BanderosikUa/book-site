from django.contrib import admin
from Authors.models import Author
from .models import Book, UserBookRelation, CommentBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_views', 'time_modified')
    search_fields = ('name', 'author')
    readonly_fields = ('time_modified', 'time_created')
    fields = ('name', 'slug', 'about', 'photo', 'author', 'genre',
              'time_created', 'time_modified',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    pass


@admin.register(CommentBook)
class CommentBookAdmin(admin.ModelAdmin):
    readonly_fields = ('time_created',)



# Register your models here.
