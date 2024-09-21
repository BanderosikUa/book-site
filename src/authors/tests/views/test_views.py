from django.test import Client, TestCase
from django.urls import reverse

from users.models import User
from books.models import Book
from authors.models import Author

class TestAuthorViews(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

        cls.author1 = Author.objects.create(name="Author1")
        cls.book1 = Book.objects.create(name='Book1', author=cls.author1)
        cls.user = User.objects.create(username='user1', password='username123', email='admifn@gmail.com')

        cls.author_url = reverse('author', args=(cls.author1.slug,))
        cls.author_all_url = reverse('all-authors')

    def test_logined_author_view_GET(self):
        """Test response from BookView based-class with logined user"""
        self.client.force_login(self.user)
        response = self.client.get(self.author_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors/author_page.html')

    def test_unlogined_author_view_GET(self):
        """Test response from BookView based-class"""
        response = self.client.get(self.author_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors/author_page.html')
        
    def test_not_found_author_view_GET(self):
        response = self.client.get(reverse('author', args=("slig", )))
        
        self.assertEquals(response.status_code, 404)
        
    def test_logined_author_all_view_GET(self):
        """Test response from BookView based-class with logined user"""
        self.client.force_login(self.user)
        response = self.client.get(self.author_all_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors/all_author_page.html')

    def test_unlogined_author_all_view_GET(self):
        """Test response from BookView based-class"""
        response = self.client.get(self.author_all_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors/all_author_page.html')

    