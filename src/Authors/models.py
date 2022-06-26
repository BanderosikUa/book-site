from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from hitcount.models import HitCount, HitCountMixin

from core.models import NameStampedModel

# Create your models here.


class Author(NameStampedModel, HitCountMixin):
    """
    The class for definiton the Author of book
    """
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_author')
    photo = models.ImageField(upload_to="authors/%Y/%m/%d",
                              default='default/author/author.png')
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("author", kwargs={"author_slug": self.slug})
