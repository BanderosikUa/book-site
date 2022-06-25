from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone

from hitcount.models import HitCount, HitCountMixin

from core.models import NameStampedModel


class Genre(NameStampedModel, HitCountMixin):
    """
    The class of book's genres
    """
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_genre')
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genres", kwargs={"genre_slug": self.slug})+'?ordering=Popular'


# class GenresShownInNavbar(models.Model):
#     genres = models.ManyToManyField(Genre)

# Create your models here.
