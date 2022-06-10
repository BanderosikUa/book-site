from Books.models import Book, UserBookRelation
from Books.views import *
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestBookViews(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

        self.model1 = Book.objects.create(name='some book')
        self.user = User.objects.create(username='user1', password='username123')

        self.book_url = reverse('book', args=(self.model1.slug,))
        self.rate_book_url = reverse('rate-book',)
        self.get_avarage_rating_url = reverse('get-avarage-rating',
                                              args=(self.model1.pk,))
        
    def test_logined_book_view_GET(self):
        """Test response from BookView based-class with logined user"""
        self.client.force_login(self.user)
        response = self.client.get(self.book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Books/main.html')

    def test_unlogined_book_view_GET(self):
        """Test response from BookView based-class"""
        response = self.client.get(self.book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Books/main.html')

    
    def test_rate_book_GET(self):
        """Test response from rate_book ajax post function"""
        self.client.force_login(self.user)
        UserBookRelation.objects.create(user=self.user, book=self.model1)

        response = self.client.post('/rate-book/',
                                    {'pk': self.model1.pk,
                                     'value': 3})

        self.assertEquals(response.status_code, 200)

    def test_get_avarage_rating_GET(self):
        """Testing response from get_avarage_rating ajax function,
        that get book_pk from url"""
        response = self.client.get(self.get_avarage_rating_url)

        self.assertEquals(response.status_code, 200)

    # def test_get_avarage_rating_without_any_relations(self):
    #     """Testing function return rating 0, if any relation exists"""
    #     response = self.client.get(self.get_avarage_rating_url)

    #     self.assertEquals(response.status_code, 200)
    #     self.assertJSONEqual(response.content, {'avg_rating': 0})
