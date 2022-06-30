from django.db import models
from unidecode import unidecode
from django.utils.text import slugify
from django.core.validators import ProhibitNullCharactersValidator, validate_slug
from django.core.exceptions import ValidationError
# Create your models here.


class NameStampedModel(models.Model):
    """
    An abstract base class model that provides
    name, slug fiels and autofill_slug function
    """
    name = models.CharField(max_length=255, db_index=True,
                            help_text='No more 255 chars',
                            validators=[ProhibitNullCharactersValidator])
    slug = models.SlugField(max_length=255,
                            blank=True,
                            null=True,
                            db_index=True,
                            validators=[validate_slug])

    class Meta:
        abstract = True

    def clean(self, *args, **kwargs):
        if not self.slug.strip():
            raise ValidationError("Author name can't be null")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            name = unidecode(self.name)
            self.slug = slugify(name)
        self.full_clean()
        super().save(*args, **kwargs)
