from datetime import datetime
from signal import default_int_handler
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
    about = models.TextField(blank=True)
    # Delete null
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
    Planning = 1
    Reading = 2
    Read = 3
    Abandonded = 4

    BOOKMARK_CHOICES = [(Planning, 'Plan to read'),
                        (Reading, 'Reading'),
                        (Read, 'Read'),
                        (Abandonded, 'Abandonded')
                        ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField(max_length=800, blank=True)
    comment_liked = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    comment_disliked = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    like = models.BooleanField(default=False)
    # Delete null after
    comment_time_created = models.DateTimeField(blank=True, null=True)
    bookmarks = models.PositiveSmallIntegerField(choices=BOOKMARK_CHOICES,
                                                 default=None, blank=True,
                                                 null=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES,
                                            default=None, blank=True,
                                            null=True)

    @property
    def comment_likes(self):
        return self.comment_liked.count()

    @property
    def comment_dislikes(self):
        return self.comment_disliked.count()


    def save(self, *args, **kwargs):
        if self.comment:
            self.comment_time_created = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}: {self.book}, RATE {self.rate}, BOOKMARK {self.BOOKMARK_CHOICES[self.bookmarks-1][1] if self.bookmarks else None}'


#class CommentBook(models.model):

# Create your models here.
