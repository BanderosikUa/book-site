from django.db import models
from django.urls import reverse
from core.models import NameStampedModel


class Genre(NameStampedModel):
    """
    The class of book's genres
    """
    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genres", kwargs={"genre_slug": self.slug})




# Create your models here.
