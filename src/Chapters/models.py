from django.db import models
from ckeditor import fields
from django.urls import reverse
from django.conf import settings

from Books.models import Book
# Create your models here.


class Chapter(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='chapters')
    title = models.CharField(max_length=150)
    body = fields.RichTextField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.name} - {self.title}"

    def get_absolute_url(self):
        return reverse('book-chapters', args=(self.book.slug,))

class BookNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    text_notification = models.TextField(max_length=500)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.book.name} - {self.user}"
