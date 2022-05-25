from django.db import models
from django.urls import reverse
from core.models import NameStampedModel
from Authors.models import Author
from Genres.models import Genre
from django.contrib.auth.models import User
from django.conf import settings


class Book(NameStampedModel):
    """
    The class for definition books.
    """
    # Delete null
    about = models.TextField(max_length=500, blank=True,
                             help_text='No more 500 words')
    # Delete null and blank
    photo = models.ImageField(upload_to='books/%Y/%m/%d/', null=True,
                              blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,
                               related_name="book_author", null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name="book_genres")
    count_views = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    readers = models.ManyToManyField(User, through='UserBookRelation',
                                     related_name="books")

    def views(self):
        """Counts new views for the book"""
        self.count_views += 1
        return self.count_views

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("book", kwargs={"slug": self.slug})


RATE_CHOICES = [(1, 'Horrible'),
                (2, 'Bad'),
                (3, 'Normal'),
                (4, 'Good'),
                (5, 'Very well')
                ]


class UserBookRelation(models.Model):
    """
    The class for rating, liking, bookmarking Book model
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, blank=True)

    def __str__(self):
        return f'{self.user.username}: {self.book}, RATE {self.rate}'


# Create your models here.
