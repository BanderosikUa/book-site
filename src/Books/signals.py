from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.test import Client

from Books.models import Book
from users.models import CustomUser
from Genres.models import Genre
from users.models import CustomUser
from Authors.models import Author

@receiver(post_save, sender=Book)
def post_save_book(created, **kwargs):
    instance = kwargs.get('instance')
    client = Client()
    if created:
        book_view_url = reverse('book', args=(instance.slug,))
        client.get(book_view_url)


@receiver(post_save, sender=Genre)
def post_save_genre(created, **kwargs):
    instance = kwargs.get('instance')
    client = Client()
    if created:
        genre_view_url = reverse('genres', args=(instance.slug,))
        client.get(genre_view_url)


# @receiver(post_save, sender=Author)
# def post_save_author(created, **kwargs):
#     instance = kwargs.get('instance')
#     client = Client()
#     if created:
#         genre_view_url = reverse('genres', args=(instance.slug,))
#         client.get(genre_view_url)
