from django.http import JsonResponse
from Books.models import Book, CommentBook, UserBookRelation
from django.db.models import Count, Q, QuerySet, Avg, FloatField, F
from django.contrib.auth.models import User
from django.db.models.functions import Round, Coalesce, Cast
from django.contrib.postgres.aggregates import ArrayAgg

class CommentBookSelector:
    """Class that fetch comment`s data from db"""

    def __init__(self, *, book_pk: int, comment_pk: int = None) -> CommentBook:
        if comment_pk:
            self.comment = CommentBook.objects.get(pk=comment_pk)
        else:
            self.comment = CommentBook.objects.filter(book__pk=book_pk)

    @property
    def user_likes(self):
        return self.comment.liked

    @property
    def user_dislikes(self):
        return self.comment.disliked

    def users_likes_filter_by_username(self, *, username: str):
        comment = self.user_likes
        return comment.filter(username=username)

    def users_dislikes_filter_by_username(self, *, username: str):
        comment = self.user_dislikes
        return comment.filter(username=username)

    @property
    def likes_amount(self):
        return self.comment.comment_likes
    
    @property
    def dislikes_amount(self):
        return self.comment.comment_dislikes
        

def get_book_relation(*, book_pk: int = None, book: Book = None) -> QuerySet:
    if book_pk:
        return UserBookRelation.objects.filter(book__pk=book_pk)
    elif book:
        return UserBookRelation.objects.filter(book=book)


def get_user_book_relation(*, book_pk: int, user: User):
    return UserBookRelation.objects.get(book__pk=book_pk,
                                        user=user)


def get_users_bookmarks_and_rating() -> Book:
    """Return users bookmarks and average rating to the book"""
    return Book.objects.annotate(
        plan_to_read=Count('userbookrelation__bookmarks',
                           filter=Q(userbookrelation__bookmarks=1)),
        reading=Count('userbookrelation__bookmarks',
                      filter=Q(userbookrelation__bookmarks=2)),
        read=Count('userbookrelation__bookmarks',
                   filter=Q(userbookrelation__bookmarks=3)),
        abandonded=Count('userbookrelation__bookmarks',
                         filter=Q(userbookrelation__bookmarks=4)),
        # Coalesce return 0 if avg rating == None
        # Cast for output_fueld error
        avg_rating=Cast(Coalesce(Round(Avg('userbookrelation__rate'),
                        precision=1), 0), output_field=FloatField()),
        comments_count=Count('comments')
        )


def get_average_rating(*, book_pk: int) -> int:
    result = Book.objects.filter(pk=book_pk).aggregate(
        avg_rating=Round(Avg('userbookrelation__rate'), precision=1)
        )
    result = result['avg_rating']
    return result if result else 0


def get_genres_of_book(*, book_pk: int) -> list:
    book = Book.objects.filter(pk=book_pk).select_related('genre')
    genres_data = list(book.values('genre__name', 'genre__slug'))    
    return genres_data
