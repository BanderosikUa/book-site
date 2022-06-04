from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from Books.models import Book, UserBookRelation
from Genres.models import Genre
from Genres.views import *


class TestBookViews(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

        self.genre1 = Genre.objects.create(name='genre1')
        self.genre2 = Genre.objects.create(name='genre2')
        self.genre3 = Genre.objects.create(name='genre3')

        self.book1 = Book.objects.create(name='some book')
        self.book1.genre.add(self.genre1, self.genre2)
        self.book2 = Book.objects.create(name='Book2')
        self.book2.genre.add(self.genre2)
        self.book3 = Book.objects.create(name='third book')
        self.book3.genre.add(self.genre3)

        self.user = User.objects.create(username='user1', password='username123')
        self.genres_url = reverse('genres', args=(self.genre2,))

    def test_genre_detail_view_GET(self):
        """Test working url of GenreDetaiView"""
        self.client.force_login(self.user)
        response = self.client.get(self.genres_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Genres/genres.html')

    def test_fetch_book_by_genre(self):
        """Test fetching correct queryset of book by genre"""
        response = list(get_books_by_genre(slug=self.genre2.slug))
        expected_repsonse = [self.book1, self.book2]

        self.assertEquals(response, expected_repsonse)
