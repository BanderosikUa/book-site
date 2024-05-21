import datetime
from django.utils import timezone
from django.test import TestCase

from books.models import Book
from apiv1.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_book(self):
        book_1 = Book.objects.create(name='Test book 1')
        data = BookSerializer(book_1).data
        expected_data = {
                'id': book_1.id,
                'name': 'Test book 1',
                'about': '',
                'photo': book_1.photo.url,
                'author': book_1.author,
                'genre': [],
                'age_category': '12',
                'time_created': data.get("time_created"),
                'time_modified': data.get("time_modified"),
                'comments': []
            }
        self.assertEquals(data, expected_data)
