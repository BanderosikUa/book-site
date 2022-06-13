from django.db.models import QuerySet


def get_book_values(qs: QuerySet) -> QuerySet:
    return qs.values('author__name', 'author__slug',
                     'name', 'pk', 'about',
                     'abandonded', 'plan_to_read',
                     'read', 'reading', 'photo',
                     'avg_rating', 'slug')
