from django.test import Client, TestCase
from django.urls import reverse

from users.models import User
from books.models import Book, UserBookRelation
from books.views import *

class TestBookViews(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

        cls.model1 = Book.objects.create(name='some book')
        cls.user = User.objects.create_user(username='user1', password='username123', email='admifn@gmail.com')

        cls.book_url = reverse('book', args=(cls.model1.slug,))
        cls.book_all_url = reverse('all-books')
        # cls.rate_book_url = reverse('rate-book',)
        # cls.get_avarage_rating_url = reverse('get-average-rating',
        #                                      args=(cls.model1.pk,))
        
    def test_logined_book_view_GET(self):
        """Test response from BookView based-class with logined user"""
        self.client.force_login(self.user)
        response = self.client.get(self.book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_page.html')

    def test_unlogined_book_view_GET(self):
        """Test response from BookView based-class"""
        response = self.client.get(self.book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_page.html')
        
    def test_logined_all_book_view_GET(self):
        """Test response from BookView based-class with logined user"""
        self.client.force_login(self.user)
        response = self.client.get(self.book_all_url)
        print(Book.objects.all().count())

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_unlogined_all_book_view_GET(self):
        """Test response from BookView based-class"""
        response = self.client.get(self.book_all_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    
    # def test_rate_book_GET(self):
    #     """Test response from rate_book ajax post function"""
    #     self.client.force_login(self.user)
    #     UserBookRelation.objects.create(user=self.user, book=self.model1)

    #     response = self.client.post('/rate-book/',
    #                                 {'pk': self.model1.pk,
    #                                  'value': 3})

    #     self.assertEquals(response.status_code, 200)

    # def test_get_avarage_rating_GET(self):
    #     """Testing response from get_avarage_rating ajax function,
    #     that get book_pk from url"""
    #     response = self.client.get(self.get_avarage_rating_url)

    #     self.assertEquals(response.status_code, 200)

    # def test_hit_count_adding(self):
    #     """Testing hitcount work"""
    #     book = Book.objects.create(name='Test book')
    #     url = reverse('book', args=(book.slug,))
    #     response = self.client.get(url)
    #     expected_hits = 2
    #     real_hits = book.hit_count.hits

    #     self.assertEquals(expected_hits, real_hits)
