from django.contrib import admin
from .models import Genre


class GenreClass(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreClass)


# Register your models here.
