from django.conf import settings
from django.db import models
from django.http import HttpRequest
from django.db.models import Count, Q
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCountMixin, HitCount
from hitcount.views import HitCountMixin

from core.models import NameStampedModel
from Authors.models import Author
from Genres.models import Genre
from users.models import CustomUser


AGE_CATEGORY = [('12', '12+'),
                ('14', '14+'),
                ('16', '16+'),
                ('18', '18+')
                ]



class Book(NameStampedModel, HitCountMixin):
    """
    The class for definition books.
    """

    
    about = models.TextField(blank=True)
    # Delete null
    photo = models.ImageField(upload_to='books/%Y/%m/%d/', 
                              default='default/book/default_book_cover_2015.jpg')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,
                               related_name="book_author", blank=True,
                               null=True)
    genre = models.ManyToManyField(Genre, blank=True,
                                   related_name="book_genres")
    age_category = models.CharField(max_length=3, choices=AGE_CATEGORY,
                                    default='12')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    readers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through='UserBookRelation',
                                     related_name="books")
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      through='CommentBook',
                                      related_name="comments")

    class Meta:
        ordering = ['-hit_count_generic__hits']

    def __str__(self):
        return f"NAME: {self.name}, AUTHOR: {self.author}," \
               f"GENRE: {list(self.genre.values_list('name', flat=True))}"


    def get_absolute_url(self):
        return reverse("book", kwargs={"book_slug": self.slug})

    # def save(self):
    # #     self.user = CustomUser.objects.get(username='admin')
    #     hit_count = HitCount.objects.get_for_object(self)
    #     request = HttpRequest()
    #     request.session = {}
    #     HitCountMixin.hit_count(request, hit_count)



RATE_CHOICES = [(1, 'Horrible'),
                (2, 'Bad'),
                (3, 'Normal'),
                (4, 'Good'),
                (5, 'Very well')
                ]

Planning = 1
Reading = 2
Read = 3
Abandoned = 4

BOOKMARK_CHOICES = [(Planning, 'Plan to read'),
                    (Reading, 'Reading'),
                    (Read, 'Read'),
                    (Abandoned, 'Abandoned')
                    ]


class UserBookRelation(models.Model):
    """
    The class for rating, liking, bookmarking Book model
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookmarks = models.PositiveSmallIntegerField(choices=BOOKMARK_CHOICES,
                                                 default=None, blank=True,
                                                 null=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES,
                                            default=None, blank=True,
                                            null=True)

    def __str__(self):
        return f'{self.user.username}: {self.book}, RATE {self.rate},' \
               f'BOOKMARK {BOOKMARK_CHOICES[self.bookmarks-1][1] if self.bookmarks else None}'


class CommentBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    body = models.TextField(max_length=800)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name='comment_likes')
    disliked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                      related_name='comment_dislikes')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.book}, {self.body[:20]}'

    @property
    def comment_likes(self):
        return self.liked.count()

    @property
    def comment_dislikes(self):
        return self.disliked.count()

# Create your models here.
