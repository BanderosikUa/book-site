from datetime import timedelta, datetime

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient

from ..models import Book
from genres.models import Genre

class BookAPITests(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.DEBUG == False:
            settings.DEBUG = True
    
    def setUp(cls):
        cls.books_url = reverse("books")

    def test_correct_age_category(self):
        age_category = '12'
        book = Book.objects.create(name="This is Going to Hurt", age_category=age_category)
        query = {
            "age_category": age_category
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.data['success'])
        self.assertEqual(age_category, response.data['results'][0]['age_category'])
        
    def test_incorrect_age_category(self):
        age_category = '12'
        book = Book.objects.create(name="This is Going to Hurt", age_category=age_category)
        query = {
            "age_category": 13
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(400, response.status_code)
        self.assertEqual(False, response.data['success'])
        self.assertEqual("Validation error", response.data['message'])
        self.assertIn("age_category", response.data['extra']['fields'])
    
    def test_correct_rating(self):
        book = Book.objects.create(name="This is Going to Hurt")
        query = {
            "rating": 0
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.data['success'])
        self.assertEqual(0, response.data['results'][0]['rating'])
    
    def test_incorrect_rating(self):
        book = Book.objects.create(name="This is Going to Hurt")
        query = {
            "rating": 5.5
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(400, response.status_code)
        self.assertEqual(False, response.data['success'])
        self.assertEqual("Validation error", response.data['message'])
        self.assertIn("rating", response.data['extra']['fields'])

    def test_correct_views(self):
        book = Book.objects.create(name="This is Going to Hurt")
        query = {
            "views": 1
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.data['success'])
        self.assertEqual(1, response.data['results'][0]['views'])
        
    def test_incorrect_views(self):
        book = Book.objects.create(name="This is Going to Hurt")
        query = {
            "views": -10
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(400, response.status_code)
        self.assertEqual(False, response.data['success'])
        self.assertEqual("Validation error", response.data['message'])
        self.assertIn("views", response.data['extra']['fields'])
        
    def test_correct_sorting(self):
        book = Book.objects.create(name="This is Going to Hurt")
        query = {
            "sorting": 1
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.data['success'])
        self.assertEqual(1, len(response.data['results']))
        
    def test_incorrect_sorting(self):
        book = Book.objects.create(name="This is Going to Hurt")
        query = {
            "sorting": 4
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(400, response.status_code)
        self.assertEqual(False, response.data['success'])
        self.assertEqual("Validation error", response.data['message'])
        self.assertIn("sorting", response.data['extra']['fields'])
    
    def test_fetching_by_name(self):
        name = "This is Going to Hurt"
        book = Book.objects.create(name=name)
        query = {
            "name": name
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.data['success'])
        self.assertEqual(name, response.data['results'][0]['name'])
        
    def test_fetching_by_genre(self):
        name = "This is Going to Hurt"
        book = Book.objects.create(name=name)
        genre_name = "Medical"
        genre = Genre.objects.create(name=genre_name)
        book.genre.add(genre)
        query = {
            "genre": genre_name
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.data['success'])
        self.assertEqual(genre_name, response.data['results'][0]['genres'][0])
        
    def test_fetching_by_date_created(self):
        time_now = datetime.now().isoformat()
        book = Book.objects.create(name="This is Going to Hurt")
        query = {
            "from_date": time_now
        }
        response = self.client.get(self.books_url, data=query)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.data['success'])
        self.assertEqual(1, len(response.data['results']))
    
