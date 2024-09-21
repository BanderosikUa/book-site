from django.urls import reverse
from django.test import RequestFactory, TestCase, Client

from hitcount.models import HitCount

from authors.models import Author
from books.models import Book, UserBookRelation, CommentBook
from users.models import User
from ...service import (
    _get_more_rated_authors,
    _get_most_viewed_authors
)

class TestAuthorServices(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client(raise_request_exception=True)
        cls.client2 = Client()
        cls.client3 = Client()
        cls.client4 = Client()
        cls.client5 = Client()

        cls.author = Author.objects.create(name='Author1')
        cls.author2 = Author.objects.create(name='Author2')
        cls.author3 = Author.objects.create(name='Author3')
        cls.author4 = Author.objects.create(name='Author4')

        cls.author_url = reverse('author', args=(cls.author.slug,))
        cls.author_url2 = reverse('author', args=(cls.author2.slug,))
        cls.author_url3 = reverse('author', args=(cls.author3.slug,))
        cls.author_url4 = reverse('author', args=(cls.author4.slug,))
        
        cls.hit_ajax = reverse('hitcount:hit_ajax')


    # def test_working_hit_count(self):
    #     self.client.get(self.author_url)
    #     self.client2.get(self.author_url)
    #     self.client3.get(self.author_url)

    #     expected_hits = 3
    #     real_hits = self.author.hit_count.hits

    #     self.assertEquals(expected_hits, real_hits)

    # def test_most_viewed_authors(self):
    #     """Testing if service function return correct author
    #     popular by the week"""
    #     expected_ordering = [self.author, self.author3, self.author2, self.author4]

    #     hit_count_obj = HitCount.objects.get_for_object(self.author)
    #     r = self.client.post(self.hit_ajax, data={'hitcountPK': str(hit_count_obj.object_pk)})
    #     self.client2.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})
    #     self.client3.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})
    #     self.client4.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})

    #     hit_count_obj = HitCount.objects.get_for_object(self.author3)
    #     self.client5.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})
    #     self.client2.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})
    #     self.client3.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})

    #     hit_count_obj = HitCount.objects.get_for_object(self.author2)
    #     self.client5.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})
    #     self.client2.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})

    #     hit_count_obj = HitCount.objects.get_for_object(self.author4)
    #     self.client.post(self.hit_ajax, data={'hitcountPK': hit_count_obj.object_pk})

    #     all_authors = Author.objects.all()
    #     real_ordering = _get_most_viewed_authors(all_authors)
    
    #     self.assertEquals(expected_ordering, real_ordering)

    def test_author_more_rated(self):
        """Testing if service function return correct author
        rated books"""
        expected_ordering = [self.author4, self.author3, self.author2, self.author]
        user1 = User.objects.create(username='abs', password='12345678', email='abs@gmail.com')
        user2 = User.objects.create(username='abs2', password='12345678', email='abs2@gmail.com') 
        user3 = User.objects.create(username='abs3', password='12345678', email='abs3@gmail.com') 
        user4 = User.objects.create(username='abs4', password='12345678', email='abs4@gmail.com') 

        book1 = Book.objects.create(name='book1', author=self.author)
        book2 = Book.objects.create(name='book2', author=self.author2)
        book3 = Book.objects.create(name='book3', author=self.author3)
        book4 = Book.objects.create(name='book4', author=self.author4)

        for book_index, book in enumerate(Book.objects.all()):
            for user_index, user in enumerate(User.objects.all()):
                UserBookRelation.objects.create(user=user, book=book, rate=book_index+1)

        all_authors = Author.objects.all()

        real_ordering = _get_more_rated_authors(all_authors)
        
        self.assertEquals(expected_ordering, real_ordering)
