from django.db.models import QuerySet

def make_dict_of_books(qs: QuerySet) -> dict:
    """Make dict that you can pass into ajax"""
    result = {}
    for book in qs:
        item = {
            'pk': book.pk,
            'absolute_url': book.get_absolute_url,
            'photo': book.photo.url,
            'author': book.author.name,
            'book_name': book.name,
            'genres': book.genre.all
            
        }
        result.append(item)


def get_book_values(qs: QuerySet) -> QuerySet:
    return qs.values('author__name', 'author__slug',
                     'name', 'pk', 'about',
                     'abandonded', 'plan_to_read',
                     'read', 'reading', 'photo',
                     'avg_rating', 'slug')


def get_comment_data(*, qs: QuerySet, ordering: str, num_books: int) -> dict:
    """Function, that return Json with limited(3) data of comments in GET ajax request"""
    visible = 3
    upper = num_books
    lower = upper - visible
    size = qs.count()
    qs = list(qs)
    return {'books': qs[lower:upper], 'size': size}
