from rest_framework.viewsets import ModelViewSet

from Books.models import Book
from Books.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
