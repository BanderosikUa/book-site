from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

from hitcount.views import HitCountDetailView, HitCountMixin

from books.services import *
from books.selectors import *
from books.forms import CommentCreateForm
from .models import Book, UserBookRelation, CommentBook


class BookView(HitCountDetailView):
    """Class-based view for displaying Book and UserBookRelation models"""
    model = Book
    template_name = "Books/book_page.html"
    slug_url_kwarg = 'book_slug'
    count_hit = True

    def get_object(self, queryset=None):
        slug = self.kwargs.get('book_slug')
        book = get_users_bookmarks_and_rating()
        return get_object_or_404(
                                book
                                .select_related('author')
                                .prefetch_related('genre', 'hit_count_generic'),
                                slug=slug
                                )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context['object']

        create_comment_form = CommentCreateForm()
        if self.request.user.is_authenticated:
            user_relation = UserBookRelation.objects.filter(book=book)\
                            .get_or_create(
                                user=self.request.user,
                                book=book)
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
        qs = get_users_bookmarks_and_rating().select_related('author')\
                                             .prefetch_related('genre', 'comments')
        qs = qs.filter(
            name__icontains=searching
        )
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
        qs = get_users_bookmarks_and_rating().select_related('author')\
                                             .prefetch_related('genre', 'comments')
        qs = qs.all()
        return order_queryset(qs=qs, ordering_by=ordering_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['ordering'] = self.request.GET.get('ordering')
        context['count'] = self.object_list.count()
        return context
