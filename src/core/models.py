from django.db import models
from unidecode import unidecode
from django.utils.text import slugify
# Create your models here.


class NameStampedModel(models.Model):
    """
    An abstract base class model that provides
    name, slug fiels and autofill_slug function
    """
    name = models.CharField(max_length=255, db_index=True,
                            help_text='No more 255 chars')
    slug = models.SlugField(max_length=255,
                            blank=True,
                            null=True,
                            db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:   
            name = unidecode(self.name)
            self.slug = slugify(name)
        super().save(*args, **kwargs)
