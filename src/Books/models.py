from django.db import models
from django.urls import reverse
from core.models import NameStampedModel
from Authors.models import Author
from Genres.models import Genre


class Book(NameStampedModel):
    """
    The class for creating, upload, comment and rating books.
    """
    # Delete null
    about = models.TextField(max_length=500, blank=True,
                             help_text='No more 500 words')
    # Delete null and blank
    photo = models.ImageField(upload_to='books/%Y/%m/%d/', null=True,
                              blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,
                               related_name="book_author", null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True,
                              blank=True, related_name="book_genre")
    count_views = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def counter(self):
        """Counts new views for the book"""
        self.count_views += 1

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("book", kwargs={"slug": self.slug})



# Create your models here.
