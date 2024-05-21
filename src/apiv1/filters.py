from django_filters import BaseInFilter, CharFilter, FilterSet

from Books.models import Book


class SlugInFilter(BaseInFilter, CharFilter):
    pass


