from django.db.models import QuerySet
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Genre


def get_book_values(qs: QuerySet) -> QuerySet:
    return qs.values('author__name', 'author__slug',
                     'name', 'pk', 'about',
                     'abandonded', 'plan_to_read',
                     'read', 'reading', 'photo',
                     'avg_rating', 'slug')


def get_all_genres_json():
    genres = Genre.objects.order_by('hit_count_generic__hits').all()[:7]
    data = []
    for genre in genres:
        item = {
            'name': genre.name,
            'url': genre.get_absolute_url(),
        }
        data.append(item)
    return {'data': data, 'all_genres_url': '#'}
