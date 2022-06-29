from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from hitcount.models import HitCount

from .models import Book, UserBookRelation, CommentBook
from Authors.models import Author
from Chapters.admin import ChapterInline

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author',
                    'time_modified', 'get_genres',
                    'get_count_views')
    search_fields = ('name', 'author__name')
    list_display_links = ('pk', 'name')
    fields = (
              'name', 'slug', 'about', 'photo',
              'get_photo_url', 'author', 'genre',
              'age_category', 'time_created',
              'time_modified', 'url_on_site')
    
    readonly_fields = ('time_modified', 'time_created',
                       'get_photo_url', 'url_on_site')
    
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ChapterInline]   

    @admin.display(description='Views')
    def get_count_views(self, obj):
        return HitCount.objects.get_for_object(obj).hits

    @admin.display(description='genres', ordering='genre__name')
    def get_genres(self, obj):
        return list(obj.genre.all())

    @admin.display(description='Photo')
    def get_photo_url(self, obj):
        return mark_safe(f"<img src='{obj.photo.url}' width=200>")
    
    @admin.display(description='Site url')
    def url_on_site(self, obj):
        url = reverse('book', args=(obj.slug,))
        return mark_safe(f"<a href='{url}'>{url}</a>")


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'bookmarks', 'rate')
    search_fields = ('user', 'book')
    

@admin.register(CommentBook)
class CommentBookAdmin(admin.ModelAdmin):
    readonly_fields = ('time_created',)



# Register your models here.
