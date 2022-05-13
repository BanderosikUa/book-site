from django.test import TestCase
from Books.models import Book
from django import setup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
setup()


class TestBookModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Book.objects.create(name='test')

    def test_name_create(self):
        book = Book.objects.get(name='test')
        assert book.name == 'test'
