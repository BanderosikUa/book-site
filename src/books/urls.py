from django.urls import path, include
from rest_framework import routers

from .views import (
    get_bookmark_data_view, get_average_rating_view, AllBookView,
    BookView, Search, get_comment_data_view, rate_book_view,
    like_book_comment_view, dislike_book_comment_view,
    bookmark_book_view, create_comment_view, delete_comment_view)
from .apis import (BookListApi, CommentListApi, CommentLikeApi,
                   CommentDislikeApi, CommentCreateApi, CommentDeleteApi)


urlpatterns = [
    path(
        "books/",
        include([
            path('<int:book_id>/comments', CommentListApi.as_view(), name="get-comments"),
            path('', BookListApi.as_view(), name="get-books"),
        ])
    ),
    path(
        "comments/",
        include([
            path('create/', CommentCreateApi.as_view(), name="comment-create"),
            path('<int:comment_id>/like', CommentLikeApi.as_view(), name="comment-like"),
            path('<int:comment_id>/dislike', CommentDislikeApi.as_view(), name="comment-dislike"),
            path('<int:comment_id>/delete', CommentDeleteApi.as_view(), name="comment-delete"),
        ])
    ),
    path('book/all/', AllBookView.as_view(), name='all-books'),
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('search/', Search.as_view(), name='search'),
    # ajax
    path('get-bookmark-data/<int:book_pk>/', get_bookmark_data_view, name='get-bookmark-data'),
    path('get-average-rating/<int:book_pk>/', get_average_rating_view, name='get-average-rating'),
    path('rate-book/', rate_book_view, name='rate-book'),
    path('bookmark-book/', bookmark_book_view, name='bookmark-book'),
    path('delete-comment/<int:comment_pk>/', delete_comment_view, name='delete-comment'),
    
]
