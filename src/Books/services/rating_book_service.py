from django.contrib.auth.models import User
from django.db.models import Avg, Count
from Books.selectors import get_book_relation, get_user_book_relation

from ..models import UserBookRelation


def get_avarage_rating(book_pk: int) -> dict:
    """Function, that calculate avarage rating of the book and
    return json into ajax function with GET request"""
    qs_user_book_relations = get_book_relation(book_pk=book_pk).aggregate(Avg('rate'))
    if qs_user_book_relations['rate__avg']:
        avarage_rating = round(qs_user_book_relations['rate__avg'], 1)
        return {'avg_rating': avarage_rating}
    else:
        return {'avg_rating': 0}


def create_rate_book(book_pk: int, rate: int, user: User) -> None:
    """Function, that add user rating into created or updated UserBookRealtion
    model and return json into ajax function with POST request"""
    user_book_relation = get_user_book_relation(book_pk=book_pk, user=user)
    user_book_relation.rate = rate
    user_book_relation.save()
