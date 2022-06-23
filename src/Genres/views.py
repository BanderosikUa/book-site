from django.core.serializers import serialize
from django.db.models import Count, F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView, MultipleObjectMixin

from hitcount.views import HitCountDetailView, DetailView

from Books.models import Book
from Books.selectors import *
from users.forms import CustomUserFormCreate
from .services import *
from .models import Genre

class GenreDetailView(HitCountDetailView, MultipleObjectMixin):
    model = Genre
    query_pk_and_slug = True
    template_name = "Genres/genres.html"
    count_hit = True
    paginate_by = 10

    def get_object(self):
        slug = self.kwargs.get('genre_slug')
        return Genre.objects.get(slug=slug)

    def get_queryset(self):
        """Get queryset by url params"""
        qs = get_users_bookmarks_and_rating().select_related('author')\
                                             .prefetch_related('genre', 'comments',
                                                               'hit_count_generic')
        qs = qs.filter(genre=self.object)
        ordering_by = self.request.GET.get('ordering')
        if ordering_by == "Novelties":
            qs = qs.order_by('-time_created')
        elif ordering_by == "Rated":
            qs = qs.order_by('-avg_rating')
        elif ordering_by == "Popular":
            qs = qs.order_by('-hit_count_generic__hits')
        return qs

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        genre_name = self.kwargs.get('genre_slug')
        context['Genre'] = genre_name
        context['books'] = self.get_queryset()
        context['ordering'] = self.request.GET.get('ordering')
        return context


def get_genres_of_book_view(request, book_pk):
    response = get_genres_of_book(book_pk=book_pk)
    print(response)
    return JsonResponse(response, safe=False)


def get_all_genres(request):
    json = get_all_genres_json()
    return JsonResponse(json)


# Create your views here.
