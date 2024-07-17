from django.urls import reverse
from django.test import TestCase, Client

from users.models import CustomUser
from books.models import Book, UserBookRelation
from genres.models import Genre
from genres.views import *


class TestBookViews(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

        cls.genre1 = Genre.objects.create(name='genre1')
        cls.genre2 = Genre.objects.create(name='genre2')
        cls.genre3 = Genre.objects.create(name='genre3')

        cls.book1 = Book.objects.create(name='some book')
        cls.book1.genre.add(cls.genre1, cls.genre2)
        cls.book2 = Book.objects.create(name='Book2')
        cls.book2.genre.add(cls.genre2)
        cls.book3 = Book.objects.create(name='third book')
        cls.book3.genre.add(cls.genre3)

        cls.user = CustomUser.objects.create(username='user1', password='username123')
        cls.genres_url = reverse('genre', args=(cls.genre2,))

    def test_genre_detail_view_GET(self):
        """Test working url of GenreDetaiView"""
        self.client.force_login(self.user)
        response = self.client.get(self.genres_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Genres/genre_page.html')
    

    def test_hit_count_adding(self):
        """Testing hitcount work"""
        response = self.client.get(self.genres_url)
        expected_hits = 2
        real_hits = self.genre2.hit_count.hits

        self.assertEquals(expected_hits, real_hits)
