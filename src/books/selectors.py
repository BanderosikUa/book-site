from datetime import timedelta

from django.http import JsonResponse
from django.db.models import Count, Q, QuerySet, Avg, FloatField, F, Value
from users.models import User
from django.db.models.functions import Round, Coalesce, Cast
from django.db.models import Min, Prefetch, Max
from django.utils import timezone

from chapters.service import get_time_verbally
from books.models import Book, CommentBook, UserBookRelation
from chapters.models import Chapter


def get_books() -> QuerySet[Book]:
    """Return users bookmarks and average rating to the book"""
    return Book.objects.annotate(
        plan_to_read=Count('userrelations__bookmarks',
                           filter=Q(userrelations__bookmarks=1)),
        reading=Count('userrelations__bookmarks',
                      filter=Q(userrelations__bookmarks=2)),
        read=Count('userrelations__bookmarks',
                   filter=Q(userrelations__bookmarks=3)),
        abandonded=Count('userrelations__bookmarks',
                         filter=Q(userrelations__bookmarks=4)),
        # Coalesce return 0 if avg rating == None
        # Cast for output_fueld error
        avg_rating=Cast(Coalesce(Round(Avg('userrelations__rate'),
                        precision=1), 0), output_field=FloatField()),
        comments_count=Count('comments', distinct=True)
        ).select_related('author').prefetch_related('genre', 'comments')


def select_books_by_chapters_created(books: QuerySet[Book]) -> QuerySet[Book]:
    three_days_ago = timezone.now()-timedelta(days=1, hours=15, seconds=3)
    chapters_with_only = (
        Chapter.objects.filter(
            time_created__gt=three_days_ago
            ).defer('body')
        )
    books = (
        books.filter(chapters__isnull=False)
        .prefetch_related(
            Prefetch('chapters', queryset=chapters_with_only)
        )
        .annotate(
            order_time=Max('chapters__time_created'),
            time=Min('chapters__time_created')
        )
        .filter(order_time__gt=three_days_ago)
        .defer('about')
        .order_by('-order_time')
    )
    return books


def order_queryset(*, qs: QuerySet, ordering_by: str) -> QuerySet[Book]:
    if ordering_by == "Novelties":
        qs = qs.order_by('-time_created')
    elif ordering_by == "Rated":
        qs = qs.order_by('-avg_rating')
    elif ordering_by == "Popular":
        qs = qs.order_by('-hit_count_generic__hits')
    return qs


def get_average_rating(book: int) -> UserBookRelation:
    relation = UserBookRelation.objects.filter(book=book).aggregate(
        avg_rating=Round(Avg('rate'), precision=1)
        )
    return relation


def get_genres_of_book(*, book_pk: int) -> list:
    book = Book.objects.filter(pk=book_pk).select_related('genre')
    genres_data = list(book.values('genre__name', 'genre__slug'))    
    return genres_data
