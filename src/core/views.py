from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic.list import ListView

from books.selectors import select_books_by_chapters_created
from authors.models import Author
from books.models import Book
from authors.service import _get_most_viewed_authors
from chapters.models import Chapter


class HomeView(ListView):
    """View for home page"""
    context_object_name = 'qs'
    template_name = 'core/home.html'

    def get_queryset(self):
        books = Book.objects.all()\
                            .defer('about', 'time_modified')
        authors = (
            Author.objects
            .all()
            .prefetch_related(Prefetch('books', queryset=books))
            .defer('biography')
        )
        # chapters = (
        #     Chapter.objects
        #     .all()
        #     .prefetch_related('book')
        #     .only('book__slug', 'book__photo', 'book__name',
        #           'title', 'time_created')
        # )
        return {
            'books': books,
            'authors': authors,
            # 'chapters': chapters
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = context['qs']['books']
        authors = context['qs']['authors']
        # chapters = context['qs']['chapters']

        context['book_novelties'] = books.order_by('-time_created')[:15]
        context['top_books'] = books.order_by('-hit_count_generic__hits')[:15]
        context['top_authors'] = _get_most_viewed_authors(authors)
        context['chapters_books'] = select_books_by_chapters_created(books)[:10]

        return context
