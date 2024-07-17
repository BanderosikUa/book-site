from django.test import Client, TestCase
from django.urls import reverse

from users.models import CustomUser
from books.models import Book
from books.views import *

class TestBookViews(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

        cls.model1 = Book.objects.create(name='some book')
        cls.user = CustomUser.objects.create(username='user1', password='username123', email='admifn@gmail.com')

        cls.book_url = reverse('book', args=(cls.model1.slug,))
        cls.rate_book_url = reverse('rate-book',)
        cls.get_avarage_rating_url = reverse('get-average-rating',
                                              args=(cls.model1.pk,))
        
    def test_logined_book_view_GET(self):
        """Test response from BookView based-class with logined user"""
        self.client.force_login(self.user)
        response = self.client.get(self.book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Books/book_page.html')

    def test_unlogined_book_view_GET(self):
        """Test response from BookView based-class"""
        response = self.client.get(self.book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Books/book_page.html')

    