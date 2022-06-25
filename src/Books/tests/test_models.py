from django.test import TestCase
from Books.models import Book
from hitcount.utils import get_hitcount_model

class TestGenreModel(TestCase):
    """Tests for Book's model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.trial = Book.objects.create(name='test book')

    def test_name_create(self):
        """Testing book's name creation"""

        real_name = getattr(self.trial, 'name')
        expected_name = 'test book'

        self.assertEqual(real_name, expected_name)

    def test_slug_autofill(self):
        """Testing slug to prepopulated from book's name"""

        real_slug = getattr(self.trial, 'slug')
        expected_name = 'test-book'

        self.assertEqual(real_slug, expected_name)

    def test_slug_autofill_cyrillic(self):
        """Testing slug to prepopulated from cyrillic book's name"""

        test = Book.objects.create(name='тест буква')
        real_slug = getattr(test, 'slug')
        expected_name = 'test-bukva'

        self.assertEqual(real_slug, expected_name)

    def test_create_defualt_hitcount_book(self):
        """Testing if add default admin hits to book"""
        expected_hits = 1

        book = Book.objects.create(name='Hello world')
        hit_count = get_hitcount_model().objects.get_for_object(book)
        real_hits = hit_count.hits

        self.assertEqual(expected_hits, real_hits)
