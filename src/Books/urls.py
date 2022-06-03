from django.urls import path

from Books.views import *

urlpatterns = [
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('author/<slug:author_slug>/', test, name='author'),
    path('genres/<slug:genre_slug>/', test, name='genres'),
    path('get-avarage-rating/<int:book_pk>/', get_avarage_rating_view, name='get-avarage-rating'),
    path('rate-book/', rate_book_view, name='rate-book'),
    path('book-comments/<int:book_pk>/<int:num_comments>/', get_comment_data_view, name='get-comment-data'),
    path('like-book-comment/', like_book_comment_view, name='like-book-comment'),
    path('dislike-book-comment/', dislike_book_comment_view, name='dislike-book-comment'),
    path('bookmark-book/', bookmark_book_view, name='bookmark-book'),
    path('get-bookmark-data/<int:book_pk>/', get_bookmark_data_view, name='get-bookmark-data'),
    path('comment-book/', create_comment_view, name='comment-book')
]
