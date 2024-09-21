from django.urls import reverse
from django.test import TestCase, Client

from users.models import User
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

        cls.user = User.objects.create(username='user1', password='username123')
        cls.book_genres_url = reverse('genre', args=(cls.genre2,))
        cls.genres_url = reverse('all-genres')

    def test_logined_book_genre_list_view_GET(self):
        """Test working url of BookGenreListView"""
        self.client.force_login(self.user)
        response = self.client.get(self.book_genres_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'genres/genre_page.html')
        
    def test_unlogined_book_genre_list_view_GET(self):
        """Test working url of BookGenreListView"""
        response = self.client.get(self.book_genres_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'genres/genre_page.html')
        
    def test_not_found_book_genre_list_view_GET(self):
        response = self.client.get(reverse('genre', args=("slig", )))
        
        self.assertEquals(response.status_code, 404)
    
    def test_logined_genre_list_view_GET(self):
        """Test working url of GenreListView"""
        self.client.force_login(self.user)
        response = self.client.get(self.genres_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'genres/all_genre_page.html')
        
    def test_unlogined_genre_list_view_GET(self):
        """Test working url of GenreListView"""
        response = self.client.get(self.genres_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'genres/all_genre_page.html')\
    

    # def test_hit_count_adding(self):
    #     """Testing hitcount work"""
    #     response = self.client.get(self.genres_url)
    #     expected_hits = 2
    #     real_hits = self.genre2.hit_count.hits

    #     self.assertEquals(expected_hits, real_hits)
