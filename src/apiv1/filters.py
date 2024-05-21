from django_filters import BaseInFilter, CharFilter, FilterSet

from books.models import Book


class SlugInFilter(BaseInFilter, CharFilter):
    pass
