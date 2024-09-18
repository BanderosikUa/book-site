from django.urls import path, include
from rest_framework import routers

from .views import (AllBookView, BookView, Search)
from .apis import (BookListApi, CommentListApi, CommentLikeApi,
                   CommentDislikeApi, CommentCreateApi, CommentDeleteApi,
                   BookmarkGetApi, BookmarkCreateApi, RatingGetApi, RatingCreateApi)


urlpatterns = [
    path(
        "books/",
        include([
            path('<int:book_id>/comments', CommentListApi.as_view(), name="get-comments"),
            path('<int:book_id>/bookmarks', BookmarkGetApi.as_view(), name="get-bookmarks"),
            path('<int:book_id>/rating', RatingGetApi.as_view(), name="get-rating"),
            path('', BookListApi.as_view(), name="get-books"),
        ])
    ),
    path(
        "comments/",
        include([
            path('create', CommentCreateApi.as_view(), name="create-comment"),
            path('<int:comment_id>/like', CommentLikeApi.as_view(), name="like-comment"),
            path('<int:comment_id>/dislike', CommentDislikeApi.as_view(), name="dislike-comment"),
            path('<int:comment_id>/delete', CommentDeleteApi.as_view(), name="delete-comment"),
        ])
    ),
    path('bookmarks/create', BookmarkCreateApi.as_view(), name="create-bookmarks"),
    path('rating/create', RatingCreateApi.as_view(), name="create-rating"),
    path('book/all/', AllBookView.as_view(), name='all-books'),
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('search/', Search.as_view(), name='search'),
    # ajax
]
