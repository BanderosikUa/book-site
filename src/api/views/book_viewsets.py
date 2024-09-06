from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from api.serializers import BookSerializer, BookListSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('name', 'genre', 'age_category')
    filterset_fields = ('genre__slug', )
    search_fields = ('name', )
    ordering_fields = ('name', 'time_created')

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        if self.action == 'retrieve':
            return BookSerializer
        return super().get_serializer_class()
