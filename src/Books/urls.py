from django.urls import path

from Books.views import BookView, test

urlpatterns = [
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('author/<slug:author_slug>/', test, name='author'),
    path('genres/<slug:genre_slug>/', test, name='genres')
]
