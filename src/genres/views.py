from django.views.generic.list import ListView

from books.selectors import order_queryset, get_books
from .models import Genre


class BookGenreListView(ListView):
    template_name = "Genres/genre_page.html"
    paginate_by = 20
    context_object_name = 'books'

    def get_queryset(self):
        """Get queryset by url params"""
        slug = self.kwargs.get('genre_slug')
        ordering_by = self.request.GET.get('ordering')
        books = get_books()
        qs = books.filter(genre__slug=slug)
        return order_queryset(qs=qs, ordering_by=ordering_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_slug = self.kwargs.get('genre_slug')
        genre = Genre.objects.get(slug=genre_slug)

        context['count'] = self.object_list.count()
        context['genre'] = genre
        context['ordering'] = self.request.GET.get('ordering')
        return context


class GenreListView(ListView):
    template_name = "Genres/all_genre_page.html"
    paginate_by = 10
    context_object_name = 'genres'

    def get_queryset(self):
        ordering_by = self.request.GET.get('ordering')
        qs = (
            Genre.objects
            .prefetch_related('books', 'hit_count_generic')
            .all()
        )
        if ordering_by == "Novelties":
            qs = qs.order_by('-time_created')
        elif ordering_by == "Popular":
            qs = qs.order_by('-hit_count_generic__hits')
        return qs

    def get_context_data(self):
        context = super().get_context_data()

        genres = context['genres']
        # for genre in genres:
        #     genre.books = genre.books.only('photo', 'slug')[:20]
        context['genres'] = genres
        context['ordering'] = self.request.GET.get('ordering')
        return context
