from django.urls import path, include
from rest_framework import routers

from .views import *
from .apis import BookListApi

urlpatterns = [
    path('book/all/', AllBookView.as_view(), name='all-books'),
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('search/', Search.as_view(), name='search'),
    # ajax
    path('get-bookmark-data/<int:book_pk>/', get_bookmark_data_view, name='get-bookmark-data'),
    path('get-average-rating/<int:book_pk>/', get_average_rating_view, name='get-average-rating'),
    path('book-comments/<int:book_pk>/<int:num_comments>/', get_comment_data_view, name='get-comment-data'),
    path('rate-book/', rate_book_view, name='rate-book'),
    path('like-book-comment/', like_book_comment_view, name='like-book-comment'),
    path('dislike-book-comment/', dislike_book_comment_view, name='dislike-book-comment'),
    path('bookmark-book/', bookmark_book_view, name='bookmark-book'),
    path('comment-book/', create_comment_view, name='comment-book'),
    path('delete-comment/<int:comment_pk>/', delete_comment_view, name='delete-comment'),
    path('books/', BookListApi.as_view(), name="get-books")
]
