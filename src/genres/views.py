from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView, MultipleObjectMixin

from core.custom_views import HitCountListView
from books.selectors import *
from .services import *
from .models import Genre

class GenreListView(HitCountListView):
    template_name = "Genres/genre_page.html"
    paginate_by = 20
    context_object_name = 'books'

    def get_queryset(self):
        """Get queryset by url params"""
        slug = self.kwargs.get('genre_slug')
        qs = (
            get_users_bookmarks_and_rating()
            .select_related('author')
            .prefetch_related('genre', 'comments',
                              'hit_count_generic')
                              )
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
        genre_slug = self.kwargs.get('genre_slug')
        genre = Genre.objects.get(slug=genre_slug)
        kwargs['hitcount_object'] = genre
        context = super().get_context_data(**kwargs)

        context['count'] = self.object_list.count()
        context['Genre'] = genre_slug
        context['ordering'] = self.request.GET.get('ordering')
        return context


class GenreAllView(ListView):
    template_name = "Genres/all_genre_page.html"
    paginate_by = 10
    context_object_name = 'genres'

    def get_queryset(self):
        qs = (
            Genre.objects
            .prefetch_related('book_genres', 'hit_count_generic')
            .all()
        )
        ordering_by = self.request.GET.get('ordering')
        if ordering_by == "Novelties":
            qs = qs.order_by('-time_created')
        elif ordering_by == "Popular":
            qs = qs.order_by('-hit_count_generic__hits')
        return qs

    def get_context_data(self):
        context = super().get_context_data()

        genres = context['genres']
        for genre in genres:
            genre.books = genre.book_genres.only('photo', 'slug')[:20]
        context['genres'] = genres
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
