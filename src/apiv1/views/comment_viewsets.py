from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from Books.models import CommentBook
from apiv1.serializers import CommentBookSerializer


class CommentBookViewSet(ModelViewSet):
    queryset = CommentBook.objects.all()
    serializer_class = CommentBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('book', )
    # filterset_fields = ('book__pk',)
    ordering_fields = ('time_created', )

    # def get_queryset(self):
    #     pk = self.kwargs.get('book_pk')
    #
    #     if pk:
    #         return CommentBook.objects.filter(book__pk=pk)
    #     return CommentBook.objects.all()