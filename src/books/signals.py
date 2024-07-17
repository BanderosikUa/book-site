from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.test import Client

from books.models import Book, UserBookRelation
from genres.models import Genre
from authors.models import Author


@receiver(post_save, sender=Book)
def post_save_book(created, **kwargs):
    """Create default hitcount and add genre is author is user"""
    instance = kwargs.get('instance')
    client = Client()
    if created:
        # hitcount
        book_view_url = reverse('book', args=(instance.slug,))
        client.get(book_view_url)
        # genre create
        if instance.author_is_user:
            genre = Genre.objects.get_or_create(name="User's")[0]
            instance.genre.add(genre)
