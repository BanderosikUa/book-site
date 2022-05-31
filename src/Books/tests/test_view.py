from django.urls import reverse
from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import User

from Books.models import Book, UserBookRelation
from Books.views import rate_book


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

    def test_book_view_GET(self):
        """Test response from BookView based-class"""
        response = self.client.get(self.book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Books/main.html')

    def test_book_view_get_count_bookmarks(self):
        """Test getting from db count of reading, abandonded, read and planning books"""
        user2 = User.objects.create(username='user2', password='username123')
        user3 = User.objects.create(username='user3', password='username123')
        relation1 = UserBookRelation.objects.create(
                    book=self.model1, user=self.user,
                    bookmarks=2
        )
        relation2 = UserBookRelation.objects.create(
                    book=self.model1, user=user2,
                    bookmarks=3
        )
        relation3 = UserBookRelation.objects.create(
                    book=self.model1, user=user3,
                    bookmarks=2
        )
        response = self.client.get(self.book_url)
        self.assertEquals(response.context_data.get('reading_users'), 2)
        self.assertEquals(response.context_data.get('read_users'), 1)



    def test_rate_book_GET(self):
        """Test response from rate_book ajax post function"""
        self.client.force_login(self.user)

        response = self.client.post('/rate-book/',
                                    {'pk': self.model1.pk,
                                     'value': 3})

        self.assertEquals(response.status_code, 200)

    def test_get_avarage_rating_GET(self):
        """Testing response from get_avarage_rating ajax function,
        that get book_pk from url"""
        response = self.client.get(self.get_avarage_rating_url)

        self.assertEquals(response.status_code, 200)

    def test_rate_book_object(self):
        """Testing created or updated UserBookRelation model"""
        self.client.force_login(self.user)
        expected_rate_value=3
        response = self.client.post('/rate-book/',
                                    {'pk': self.model1.pk,
                                     'value': expected_rate_value})
        relation = UserBookRelation.objects.get(
                   book=self.model1, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(relation.rate, expected_rate_value)

    def test_get_avarage_rating_without_any_relations(self):
        """Testing if function return rating 0, if any relation exists"""
        response = self.client.get(self.get_avarage_rating_url)

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content, {'avg_rating': 0})

    def test_get_avarage_rating_with_3_relations(self):
        """Testing if function return rating 0, if any relation exists"""
        user2 = User.objects.create(username='user2', password='username123')
        user3 = User.objects.create(username='user3', password='username123')
        relation1 = UserBookRelation.objects.create(
                    book=self.model1, user=self.user,
                    rate=2
        )
        relation2 = UserBookRelation.objects.create(
                    book=self.model1, user=user2,
                    rate=5
        )
        relation3 = UserBookRelation.objects.create(
                    book=self.model1, user=user3,
                    rate=2
        )

        response = self.client.get(self.get_avarage_rating_url)
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content, {'avg_rating': 3,
                                                'user_rating_count': 3})
    
    def test_get_comment_data(self):
        
