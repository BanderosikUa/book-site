from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.pagination import LimitOffsetPagination, get_paginated_response
from users.serializers import UserSerializer

from .models import CommentBook, Book, AGE_CATEGORY
from .serializers import OutputReactionSerializer
from .services import (list_books, like_comment, dislike_comment,
                       )


class BookListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100
    
    class OutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField()
        genres = serializers.SerializerMethodField()
        views = serializers.SerializerMethodField()
        rating = serializers.SerializerMethodField()
        
        class Meta:
            model = Book
            fields = ['id', 'name', 'author', 'genres', 
                      'age_category', 'time_created',
                      'time_modified', 'views', 'rating']
            
        def get_author(self, obj):
            if obj.author:
                return obj.author.name
            else:
                return None
        
        def get_genres(self, obj):
            return list(obj.genre.values_list("name", flat=True))
        
        def get_views(self, obj):
            return obj.hit_count.hits
        
        def get_rating(self, obj):
            return obj.avg_rating
    
    class FilterSerializer(serializers.Serializer):
        from_date = serializers.DateTimeField(required=False)
        to_date = serializers.DateTimeField(required=False)
        sorting = serializers.ChoiceField(required=False, choices=(1, 2, 3))
        genre = serializers.CharField(required=False)
        name = serializers.CharField(required=False)
        author = serializers.CharField(required=False)
        age_category = serializers.ChoiceField(required=False, choices=AGE_CATEGORY)
        views = serializers.IntegerField(required=False, min_value=0)
        rating = serializers.DecimalField(required=False, max_digits=3, decimal_places=2,
                                          min_value=0, max_value=5)
        
    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        books = list_books(filters=filters_serializer.validated_data)

        response = get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=books,
            request=request,
            view=self
        )

        return response


class CommentListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 3
    
    class OutputSerializer(serializers.ModelSerializer):
        def __init__(self, instance=None, data=..., **kwargs):
            super().__init__(instance, data, **kwargs)
            request = self.context.get('request', None)
            self.user = request.user if request else None
        
        user = UserSerializer()
        comment = serializers.CharField(source="body")
        likes = serializers.IntegerField(source="comment_likes")
        dislikes = serializers.IntegerField(source="comment_dislikes")
        liked = serializers.SerializerMethodField()
        disliked = serializers.SerializerMethodField()
        is_creator = serializers.SerializerMethodField()
        
        class Meta:
            model = CommentBook
            fields = ['id', 'user', 'comment',
                      'likes', 'dislikes', 'time_created',
                      'liked', 'disliked', 'is_creator']
        
        def get_liked(self, obj):
            return True if self.user in obj.liked.all() else False
        
        def get_disliked(self, obj):
            return True if self.user in obj.disliked.all() else False
        
        def get_is_creator(self, obj):
            return obj.user == self.user
        
    def get(self, request, book_id):
        comments = CommentBook.objects.select_related('user').filter(book=book_id)
        # print(comments.values())

        response = get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=comments,
            request=request,
            view=self
        )

        return response


class CommentLikeApi(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, comment_id):
        comment = CommentBook.objects.prefetch_related('liked', 'disliked')\
                                     .get(id=comment_id)
        comment = like_comment(comment, request.user)
        
        data = OutputReactionSerializer(comment, context={'request': request}).data
        
        return Response(data)
    
    
class CommentDislikeApi(APIView):
    permission_classes = (IsAuthenticated, )

    
    def get(self, request, comment_id):
        comment = CommentBook.objects.prefetch_related('liked', 'disliked')\
                                     .get(id=comment_id)
        comment = dislike_comment(comment, request.user)
        
        data = OutputReactionSerializer(comment, context={'request': request}).data
        
        return Response(data)
        

# def like_book_comment_view(request):
#     """Function, that add or remove user like to book's comment
#     and return Json in POST ajax request"""
#     comment_pk = request.POST.get('comment_pk')
#     book_pk = request.POST.get('book_pk')
#     user = request.user if request.user.is_authenticated else None
#     if user:
#         response = like_book_comment(comment_pk=comment_pk,
#                                      book_pk=book_pk,
#                                      user=user)
#         return JsonResponse(response)
#     else:
#         return JsonResponse({'user': False})


# def dislike_book_comment_view(request):
#     """Function, that add or remove user dislike to book's comment
#     and return Json in POST ajax request"""
#     comment_pk = request.POST.get('comment_pk')
#     book_pk = request.POST.get('book_pk')
#     user = request.user if request.user.is_authenticated else None
#     if user:
#         response = dislike_book_comment(comment_pk=comment_pk, 
#                                         book_pk=book_pk,
#                                         user=user)
#         return JsonResponse(response)
#     else:
#         return JsonResponse({'user': False})


# def create_comment_view(request):
#     """Function, that create comment model from AJAX post request"""
#     book_pk = request.POST.get('book_pk')
#     body = request.POST.get('comment')
#     user = request.user if request.user.is_authenticated else None
#     if user:
#         response = create_comment(book_pk=book_pk, body=body, user=user)
#         return JsonResponse(response)
#     else:
#         return JsonResponse({'user': False})
    

# def bookmark_book_view(request):
#     """Function, that add or remove user bookmark and return selected bookmark"""
#     book_pk = request.POST.get('book_pk')
#     bookmark = int(request.POST.get('bookmarked'))
#     user = request.user if request.user.is_authenticated else None
#     if user:
#         response = bookmark_book(book_pk=book_pk, bookmark=bookmark, user=user)
#         return JsonResponse(response)
#     else:
#         return JsonResponse({'user': False})


# def get_bookmark_data_view(request, book_pk):
#     """Function, that return selected user bookmark"""
#     if request.user.is_authenticated:
#         response = get_bookmark_data(book_pk=book_pk, user=request.user)
#         return JsonResponse(response)
#     else:
#         return JsonResponse({'user': False})


# def delete_comment_view(request, comment_pk):
#     """Function that delete comment"""
#     user = request.user
#     response = delete_book(
#         comment_pk=comment_pk,
#         user=user
#         )
#     return JsonResponse(response)
    
