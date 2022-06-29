from django.urls import path
from .views import *


urlpatterns = [
    path('genre/all/', GenreAllView.as_view(), name='all-genres'),
    path('genre/<slug:genre_slug>/', GenreListView.as_view(), name='genre'),
    path('books/get-genres-of-book/<int:book_pk>/', get_genres_of_book_view, name='get-genres-of-book'),
    path('get-genres/', get_all_genres, name='get-all-genres'),
]
