from Books.models import Book
from Books.selectors import *
from .services import *

from django.core.serializers import serialize
from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render 
from django.urls import reverse
from django.views.generic.list import ListView


class GenreDetailView(ListView):
    template_name = "Genres/genres.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        """Get queryset by url params"""
        slug = self.kwargs.get('genre_slug')
        qs = get_users_bookmarks_and_rating().filter(genre__slug=slug)
        qs = qs.select_related('author').prefetch_related('genre', 'hit_count_generic')
        ordering_by = self.request.GET.get('ordering')
        if ordering_by == "Novelties":
            qs = qs.order_by('-time_created')
        elif ordering_by == "Rated":
            qs = qs.order_by('-avg_rating')
        elif ordering_by == "Popular":
            qs = qs.order_by('-hit_count_generic__hits')
            print(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_name = self.kwargs.get('genre_slug')
        context['Genre'] = genre_name
        context['ordering'] = self.request.GET.get('ordering')
        return context


class JsonGenreDetailView(ListView):
    """Return book's by genre in order by time created"""
    template_name = "Genres/genres.html"
    context_object_name = "books"
    
    def get_queryset(self):
        """Get queryset by time created"""
        slug = self.kwargs.get('genre_slug')
        qs = get_users_bookmarks_and_rating().filter(genre__slug=slug)
        qs = qs.select_related('author').prefetch_related('genre')
        qs = qs.order_by('-time_created')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_name = self.kwargs.get('genre_slug')
        context['Genre'] = genre_name
        return context

    def get(self, *args, **kwargs):
        self.object_list = None
        return render(self.request, self.template_name,
                      {'Genre': self.kwargs.get('genre_slug')})

    def post(self, *args, **kwargs):
        """Method for ajax that return JsonResponse with sorted qs"""
        if self.request.method == 'POST':
            target = self.request.POST.get('ordering_by')
            if target == 'Rated':
                qs = get_book_values(self.get_queryset()).order_by('-avg_rating')
            elif target == 'Novelties':
                qs = get_book_values(self.get_queryset())
            qs = list(qs)
            return JsonResponse({'books': qs})


def get_genres_of_book_view(request, book_pk):
    response = get_genres_of_book(book_pk=book_pk)
    print(response)
    return JsonResponse(response, safe=False)

# Create your views here.
