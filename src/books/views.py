from typing import Any
from django.http import HttpRequest, HttpResponse
from silk.profiling.profiler import silk_profile

from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from hitcount.views import HitCountDetailView

from books.selectors import get_books, order_queryset
from books.forms import CommentCreateForm
from .models import Book, UserBookRelation


class BookView(DetailView):
    """Class-based view for displaying Book and UserBookRelation models"""
    model = Book
    template_name = "Books/book_page.html"
    slug_url_kwarg = 'book_slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('book_slug')
        books = get_books()
        book = get_object_or_404(
            books.prefetch_related('hit_count_generic'),
            slug=slug
        )
        return book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context['object']

        create_comment_form = CommentCreateForm()
        if self.request.user.is_authenticated:
            user_relation = UserBookRelation.objects.filter(book=book)\
                                                    .get_or_create(
                                                        user=self.request.user,
                                                        book=book
                                                        )
            context['user_relation'] = user_relation[0]
        
        context['Book'] = book
        context['comment_create_form'] = create_comment_form
        return context


class Search(ListView):
    """Search books"""
    paginate_by = 20
    context_object_name = 'books'

    def get_queryset(self):
        searching = self.request.GET.get('q')
        ordering_by = self.request.GET.get('ordering')
        books = get_books()
        qs = books.filter(name__icontains=searching)
        return order_queryset(qs=qs, ordering_by=ordering_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['ordering'] = self.request.GET.get('ordering')
        context['count'] = self.object_list.count()
        return context


class AllBookView(ListView):
    """Display all books"""
    paginate_by = 20
    context_object_name = 'books'

    def get_queryset(self):
        ordering_by = self.request.GET.get('ordering')
        books = get_books()
        qs = books.all()
        return order_queryset(qs=qs, ordering_by=ordering_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['ordering'] = self.request.GET.get('ordering')
        context['count'] = self.object_list.count()
        return context
