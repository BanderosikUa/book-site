from django.template.defaulttags import register


@register.filter
def get_book_key(book_pk):
    return f'book-{book_pk}'
