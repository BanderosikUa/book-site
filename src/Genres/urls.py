from django.urls import path
from .views import GenreDetailView
from .views import *


urlpatterns = [
    path('genres/all/', GenreAllView.as_view(), name='all-genres'),
    path('genres/<slug:genre_slug>/', GenreDetailView.as_view(), name='genres'),
    path('books/get-genres-of-book/<int:book_pk>/', get_genres_of_book_view, name='get-genres-of-book'),
    path('get-genres/', get_all_genres, name='get-all-genres'),
]
