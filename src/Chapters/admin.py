from django.contrib import admin
from .models import Chapter

# Register your models here.


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    fields = ('pk', 'book', 'title', 'body', 'time_created', 'time_modified')
    readonly_fields = ('pk', 'book','time_created', 'time_modified')


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0
    fields = ['title', 'body']
