from django.urls import path

from Books.views import BookView, get_avarage_rating, rate_book, test, get_comment_data

urlpatterns = [
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('author/<slug:author_slug>/', test, name='author'),
    path('genres/<slug:genre_slug>/', test, name='genres'),
    path('get-avarage-rating/<int:book_pk>/', get_avarage_rating, name='get-avarage-rating'),
    path('rate-book/', rate_book, name='rate-book'),
    path('book-comments/<int:book_pk>/<int:num_comments>/', get_comment_data, name='get-comment-data')
]
