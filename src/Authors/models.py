from django.db import models
from django.urls import reverse
from core.models import NameStampedModel

# Create your models here.


class Author(NameStampedModel):
    """
    The class for definiton the Author of book
    """
    photo = models.ImageField(upload_to="authors/%Y/%m/%d",
                              null=True, blank=True)
    biography = models.TextField(max_length=300, blank=True,
                                 help_text="No more 300 words")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("author", kwargs={"author_slug": self.slug})
