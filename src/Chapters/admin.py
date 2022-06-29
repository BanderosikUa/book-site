from django.contrib import admin
from .models import Chapter

# Register your models here.


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0
    fields = ['title', 'body']
