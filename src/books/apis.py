from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import LimitOffsetPagination, get_paginated_response

from .models import CommentBook
from .services.comment_book_service import get_comment_data, like_book_comment


class CommentListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 3
    
    class OutputSerializer(serializers.ModelSerializer):
        username = serializers.CharField(source="user.username")
        avatar = serializers.URLField(source="user.avatar.url")
        user_url = serializers.URLField(source="user.get_absolute_url")
        
        class Meta:
            model = CommentBook
            fields = ['id', 'username', 'avatar', 'user_url', 'body',
                      ]
    
    
    def get(self, request):
        pass


def get_comment_data_view(request, book_pk, num_comments):
    """Function, that return Json with limited(3) data of comments in GET ajax request"""
    user = request.user
    response = get_comment_data(book_pk=book_pk,
                                num_comments=num_comments,
                                user=user)
    return JsonResponse(response)


def like_book_comment_view(request):
    """Function, that add or remove user like to book's comment
    and return Json in POST ajax request"""
    comment_pk = request.POST.get('comment_pk')
    book_pk = request.POST.get('book_pk')
    user = request.user if request.user.is_authenticated else None
    if user:
        response = like_book_comment(comment_pk=comment_pk,
                                     book_pk=book_pk,
                                     user=user)
        return JsonResponse(response)
    else:
        return JsonResponse({'user': False})


def dislike_book_comment_view(request):
    """Function, that add or remove user dislike to book's comment
    and return Json in POST ajax request"""
    comment_pk = request.POST.get('comment_pk')
    book_pk = request.POST.get('book_pk')
    user = request.user if request.user.is_authenticated else None
    if user:
        response = dislike_book_comment(comment_pk=comment_pk, 
                                        book_pk=book_pk,
                                        user=user)
        return JsonResponse(response)
    else:
        return JsonResponse({'user': False})


def create_comment_view(request):
    """Function, that create comment model from AJAX post request"""
    book_pk = request.POST.get('book_pk')
    body = request.POST.get('comment')
    user = request.user if request.user.is_authenticated else None
    if user:
        response = create_comment(book_pk=book_pk, body=body, user=user)
        return JsonResponse(response)
    else:
        return JsonResponse({'user': False})
    

def bookmark_book_view(request):
    """Function, that add or remove user bookmark and return selected bookmark"""
    book_pk = request.POST.get('book_pk')
    bookmark = int(request.POST.get('bookmarked'))
    user = request.user if request.user.is_authenticated else None
    if user:
        response = bookmark_book(book_pk=book_pk, bookmark=bookmark, user=user)
        return JsonResponse(response)
    else:
        return JsonResponse({'user': False})


def get_bookmark_data_view(request, book_pk):
    """Function, that return selected user bookmark"""
    if request.user.is_authenticated:
        response = get_bookmark_data(book_pk=book_pk, user=request.user)
        return JsonResponse(response)
    else:
        return JsonResponse({'user': False})


def delete_comment_view(request, comment_pk):
    """Function that delete comment"""
    user = request.user
    response = delete_book(
        comment_pk=comment_pk,
        user=user
        )
    return JsonResponse(response)
    
