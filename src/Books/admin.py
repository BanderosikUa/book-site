from django.contrib import admin
from Authors.models import Author
from .models import Book, UserBookRelation, CommentBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'time_modified', 'get_genres', 'get_count_views')
    search_fields = ('name', 'author')
    readonly_fields = ('time_modified', 'time_created', )
    fields = ('name', 'slug', 'about', 'photo', 'author', 'genre',
              'time_created', 'time_modified',)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description='Views')
    def get_count_views(self, obj):
        return obj.count_views

    @admin.display(description='genres', ordering='genre__name')
    def get_genres(self, obj):
        return list(obj.genre.all())


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'bookmarks', 'rate')
    search_fields = ('user', 'book')
    

@admin.register(CommentBook)
class CommentBookAdmin(admin.ModelAdmin):
    readonly_fields = ('time_created',)



# Register your models here.
