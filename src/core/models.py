from django.db import models
from unidecode import unidecode
from django.utils.text import slugify
# Create your models here.


class NameStampedModel(models.Model):
    """
    An abstract base class model that provides
    name, slug fiels and autofill_slug function
    """
    name = models.CharField(max_length=100, db_index=True,
                            help_text='No more 100 chars')
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            name = unidecode(self.name)
            self.slug = slugify(name)
        super().save(*args, **kwargs)
