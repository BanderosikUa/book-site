from django.db import models
from core.models import NameStampedModel


class Genre(NameStampedModel):

    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"

    def __str__(self):
        return self.name



# Create your models here.
