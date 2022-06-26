from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy, reverse

from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'slug')
    fields = ("name", "slug", "photo", "get_photo_url", "biography", "get_author_books", "url_on_site")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('get_photo_url', 'get_author_books', 'url_on_site')

    @admin.display(description='Photo')
    def get_photo_url(self, obj):
        return mark_safe(f"<img src='{obj.photo.url}' width=50>")

    @admin.display(description='Books')
    def get_author_books(self, obj):
        books = obj.book_author.all()
        if books:
            html = '<ul>'
            for book in books:
                html += f"<li><a href='{reverse_lazy('admin:Books_book_change', args=(book.id,))}'>{book.name}</a></li>"
            html += '</ul>'
        else:
            html = 'No any books'
        return mark_safe(html)

    @admin.display(description='Site url')
    def url_on_site(self, obj):
        url = reverse('author', args=(obj.slug,))
        return mark_safe(f"<a href='{url}'>{url}</a>")
# Register your models here.
