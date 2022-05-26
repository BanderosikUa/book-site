from django.test import TestCase
from Books.models import Book


class TestBookModel(TestCase):
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
