from django.urls import path

from .views import BookGenreListView, GenreListView
from .apis import GenresNameListApi


urlpatterns = [
    path('genres/all/', GenreListView.as_view(), name='all-genres'),
    path('genres/all/names/', GenresNameListApi.as_view(), name='get-genres-names'),
    path('genres/<slug:genre_slug>/', BookGenreListView.as_view(), name='genre'),
]
