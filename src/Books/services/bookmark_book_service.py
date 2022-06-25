from django.contrib.auth.models import User
from ..models import CommentBook
from ..selectors import CommentBookSelector, get_user_book_relation


def bookmark_book(*, book_pk: int, user: User, bookmark: int):
    """Function, that add or remove user bookmark and return selected bookmark"""
    user_relation = get_user_book_relation(book_pk=book_pk, user=user)
    previous_bookmark = user_relation.bookmarks
    clicked = True
    if previous_bookmark == bookmark:
        clicked = False
        user_relation.bookmarks = None
    else:
        user_relation.bookmarks = bookmark
    user_relation.save()
    return {'clicked': clicked, 'previous_bookmark': previous_bookmark, 'user': True}


def get_bookmark_data(*, book_pk: int, user: User):
    """Function, that return selected user bookmark"""
    relation = get_user_book_relation(book_pk=book_pk, user=user)
    return {'bookmark_value': relation.bookmarks, 'user': True}
