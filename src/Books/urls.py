from django.urls import path, include

from Books.views import *


urlpatterns = [
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('get-average-rating/<int:book_pk>/', get_average_rating_view, name='get-average-rating'),
    path('rate-book/', rate_book_view, name='rate-book'),
    path('book-comments/<int:book_pk>/<int:num_comments>/', get_comment_data_view, name='get-comment-data'),
    path('like-book-comment/', like_book_comment_view, name='like-book-comment'),
    path('dislike-book-comment/', dislike_book_comment_view, name='dislike-book-comment'),
    path('bookmark-book/', bookmark_book_view, name='bookmark-book'),
    path('get-bookmark-data/<int:book_pk>/', get_bookmark_data_view, name='get-bookmark-data'),
    path('comment-book/', create_comment_view, name='comment-book'),
    path('search/', Search.as_view(), name='search'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount'))
]
