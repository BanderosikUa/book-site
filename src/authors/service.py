from datetime import timedelta

from django.db.models import F, Count, QuerySet, FloatField, Avg, Sum, When, Exists, Value, Case, Q
from django.utils import timezone
from django.db.models.functions import Round, Coalesce, Cast
from django.contrib.postgres.aggregates.general import ArrayAgg

def get_tops_dict(object_list: QuerySet) -> list:
    """Return list of dicts with name and queryset author's tops """
    tops = []
    top_by_book = _get_top_authors_by_books(object_list)
    most_viewed_top = _get_most_viewed_authors(object_list)
    rated_top = _get_more_rated_authors(object_list)
    
    most_viewed_dict = {
        'name': 'Most view authors by a month',
        'ordering': most_viewed_top
        }
    top_author_by_books_dict = {
        'name': "Top authors by them's books",
        'ordering': top_by_book
        }
    rated_top_dict = {
        'name': 'Most rated authors!',
        'ordering': rated_top
        }
    
    tops.append(most_viewed_dict)
    tops.append(top_author_by_books_dict)
    tops.append(rated_top_dict)
    return tops

def _get_most_viewed_authors(object_list: QuerySet) -> list:
    """Return list of 10 most popular author by a month"""
    period_month = timezone.now() - timedelta(days=30)
    ordering = object_list.filter(
        hit_count_generic__hit__created__gte=period_month)\
        .annotate(
            counts=F('hit_count_generic__hits'),
            genres=ArrayAgg(F('book_author__genre__name'),
                            distinct=True)
        ).order_by('-counts')[:10]
    return list(ordering)


def _get_more_rated_authors(object_list: QuerySet) -> list:
    """Return list of more rated authors"""
    ordering = object_list.annotate(
        rate=Cast(
            Coalesce(
                Round(
                    Avg('book_author__userbookrelation__rate'),
                    precision=1), 0),
            output_field=FloatField()),
        genres=ArrayAgg(
            F('book_author__genre__name'),
            distinct=True)
        ).order_by('-rate')[:10]
    return list(ordering)


def _get_top_authors_by_books(object_list: QuerySet):
    ordering = object_list.filter(book_author__isnull=False)\
                          .annotate(
        hits_all_books=Sum('book_author__hit_count_generic__hits'),
        genres=ArrayAgg(F('book_author__genre__name'),
                        distinct=True)
        ).order_by('-hits_all_books')[:10]
    return list(ordering)
