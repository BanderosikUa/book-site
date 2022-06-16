from attr import attr
from users.forms import CustomUserFormCreate
from Books.models import Book
from Books.selectors import *
from .services import *

from django.core.serializers import serialize
from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render 
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView

class GenreDetailView(ListView):
    template_name = "Genres/genres.html"
    context_object_name = "books"
    form_class = CustomUserFormCreate()
    paginate_by = 10
    form_create_user = CustomUserFormCreate()

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
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_name = self.kwargs.get('genre_slug')
        context['Genre'] = genre_name
        context['ordering'] = self.request.GET.get('ordering')
        context['form_create_user'] = self.form_create_user
        return context

    def post(self, request, *args, **kwargs):
        form = CustomUserFormCreate(request.POST)
        slug = kwargs.get('genre_slug')
        if form.is_valid():
            print('ok')
            print(form.cleaned_data)
        else:
            form_error = True
        return redirect('genres', genre_slug=slug)
    


def get_genres_of_book_view(request, book_pk):
    response = get_genres_of_book(book_pk=book_pk)
    print(response)
    return JsonResponse(response, safe=False)

# Create your views here.
