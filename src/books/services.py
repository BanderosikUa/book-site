from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from users.models import User

from .models import Book, CommentBook, UserBookRelation
from .selectors import get_books

from .filters import BaseBookFilter

def list_books(*, filters=None) -> QuerySet[Book]:
    filters = filters or {}
    
    qs = (get_books()
          .select_related('author')
          .prefetch_related('genre', 'comments', 'hit_count_generic'))
      
    qs = BaseBookFilter(filters, qs).qs
    if "sorting" in filters:
        sorting = filters['sorting']

        if sorting == 1:
            # novelties
            qs = qs.order_by('-time_created')
        elif sorting == 2:
            # popular
            qs = qs.order_by('-hit_count_generic__hits')
        elif sorting == 3:
            # rated
            qs = qs.order_by('-avg_rating')
        
    return qs


def like_comment(comment: CommentBook, user: User) -> CommentBook:
    if comment.liked.filter(id=user.id).exists():
        comment.liked.remove(user)
    elif comment.disliked.filter(id=user.id).exists():
        comment.disliked.remove(user)
        comment.liked.add(user)
    else:
        comment.liked.add(user)
    return comment


def dislike_comment(comment: CommentBook, user: User) -> CommentBook:
    if comment.disliked.filter(id=user.id).exists():
        comment.disliked.remove(user)
    elif comment.liked.filter(id=user.id).exists():
        comment.liked.remove(user)
        comment.disliked.add(user)
    else:
        comment.disliked.add(user)
    return comment


def create_comment(user: User, book: int, body: str) -> CommentBook:
    comment = CommentBook.objects.create(book_id=book, user=user,
                                         body=body)
    return comment


def create_bookmark(user: User, book: int, bookmarks: int) -> UserBookRelation:
    relation, _ = UserBookRelation.objects.get_or_create(book_id=book, user=user)
    
    if relation.bookmarks == bookmarks:
        relation.bookmarks = None
    else:
        relation.bookmarks = bookmarks
    relation.save(update_fields=["bookmarks"])
    return relation


def create_rate(user: User, book: int, rate: int) -> UserBookRelation:
    relation, _ = UserBookRelation.objects.get_or_create(book_id=book, user=user)
    
    relation.rate = rate
    relation.save(update_fields=["rate"])
    return relation
