from django.contrib.auth.models import User
from django.db.models import Avg, Count
from Books.selectors import *
from ..models import Book


# def get_average_rating(book_pk: int) -> dict:
#     """Function, that calculate avarage rating of the book and
#     return json into ajax function with GET request"""
#     average_rating = get_average_rating(book_pk=book_pk)
#     return {'avg_rating': average_rating}


def create_rate_book(book_pk: int, rate: int, user: User) -> dict:
    """Function, that add user rating into created or updated UserBookRealtion
    model and return json into ajax function with POST request"""
    if user:
        user_book_relation = get_user_book_relation(book_pk=book_pk, user=user)
        user_book_relation.rate = rate
        user_book_relation.save()
        return {'user': True}
    else:
        return {'user': False}
