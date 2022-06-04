from django.shortcuts import render
from django.views.generic.list import ListView
from Books.selectors import get_books_by_genre
from Books.models import Book


class GenreDetailView(ListView):
    """Return book's by genre in order by time created"""
    
    template_name = "Genres/genres.html"

    def get_queryset(self):
        slug = self.kwargs.get('genre_slug')
        qs = get_books_by_genre(slug=slug)
        qs = qs.order_by('-time_created')
        return qs

    def get():
        pass


# Create your views here.
