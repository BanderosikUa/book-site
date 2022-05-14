from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Book(models.Model):
    """
    The class for creating, upload, comment and rating books.
    """

    name = models.CharField(max_length=100, db_index=True,
                            help_text='No more 100 chars')
    slug = models.SlugField(null=True, blank=True)
    # Delete null
    about = models.TextField(max_length=500, null=True, blank=True,
                             help_text='No more 500 strings')
    # Delete null and blank
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True,
                              blank=True)
    author = models.CharField(max_length=100, db_index=True,)
    count_views = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)




    def counter(self):
        """Counts new views for the book"""
        self.count_views += 1

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        name = unidecode(self.name)
        self.slug = slugify(name)
        super().save(*args, **kwargs)



# Create your models here.
