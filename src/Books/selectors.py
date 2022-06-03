from Books.models import Book, CommentBook, UserBookRelation
from django.db.models import Count, Q, QuerySet
from django.contrib.auth.models import User


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


def get_users_bookmarks(*, book: Book = None, book_pk: int = None) -> dict:
    if book:
        relations = get_book_relation(book=book)
    elif book_pk:
        relations = get_book_relation(book_pk=book_pk)
        
    return relations.aggregate(
                        plan_to_read=Count('bookmarks', filter=Q(bookmarks=1)),
                        reading=Count('bookmarks', filter=Q(bookmarks=2)),
                        read=Count('bookmarks', filter=Q(bookmarks=3)),
                        abandonded=Count('bookmarks', filter=Q(bookmarks=4))
                        )
