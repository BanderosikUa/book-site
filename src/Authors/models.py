from django.db import models
from core.models import NameStampedModel

# Create your models here.


class Author(NameStampedModel):
    photo = models.ImageField(upload_to="authors/%Y/%m/%d",
                              null=True, blank=True)
    biography = models.TextField(max_length=300, blank=True,
                                 help_text="No more 300 words")

    def __str__(self):
        return self.name
