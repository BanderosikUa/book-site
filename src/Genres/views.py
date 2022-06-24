from django.core.serializers import serialize
from django.db.models import Count, F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView, MultipleObjectMixin

from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from Books.models import Book
from Books.selectors import *
from users.forms import CustomUserFormCreate
from .services import *
from .models import Genre

class GenreDetailView(ListView):
    template_name = "Genres/genre_page.html"
    paginate_by = 20
    context_object_name = 'books'

    def get_queryset(self):
        """Get queryset by url params"""
        slug = self.kwargs.get('genre_slug')
        qs = get_users_bookmarks_and_rating().select_related('author')\
                                             .prefetch_related('genre', 'comments',
                                                               'hit_count_generic')
        qs = qs.defer('readers', 'time_created', 'age_category')
        qs = qs.filter(genre__slug=slug)
        ordering_by = self.request.GET.get('ordering')
        if ordering_by == "Novelties":
            qs = qs.order_by('-time_created')
        elif ordering_by == "Rated":
            qs = qs.order_by('-avg_rating')
        elif ordering_by == "Popular":
            qs = qs.order_by('-hit_count_generic__hits')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_slug = self.kwargs.get('genre_slug')
        genre = Genre.objects.get(slug=genre_slug)
        # add hitcount to genre
        hit_count = HitCount.objects.get_for_object(genre)
        hit_count_response = HitCountMixin.hit_count(self.request, hit_count)

        context['Genre'] = genre_slug
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
