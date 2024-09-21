# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.urls import reverse
# from django.test import Client

# from .models import Author


# @receiver(post_save, sender=Author)
# def post_save_author(created, **kwargs):
#     instance = kwargs.get('instance')
#     client = Client()
#     if created:
#         genre_view_url = reverse('author', args=(instance.slug,))
#         client.get(genre_view_url)
