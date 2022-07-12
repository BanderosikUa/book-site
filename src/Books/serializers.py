from rest_framework import serializers

from Books.models import Book
from Books.models import UserBookRelation


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'bookmarks', 'rate')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('author_is_user', 'slug')
