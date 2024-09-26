from django.shortcuts import get_object_or_404

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.pagination import LimitOffsetPagination, get_paginated_response
from api.permissions import IsAuthor

from .models import CommentBook, Book, AGE_CATEGORY, UserBookRelation
from .serializers import CommentSerializer, BookShortSerializer
from .services import (list_books, like_comment, dislike_comment,
                       create_comment, create_bookmark, create_rate)
from .selectors import get_average_rating


class BookListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100

    class FilterSerializer(serializers.Serializer):
        from_date = serializers.DateTimeField(required=False)
        to_date = serializers.DateTimeField(required=False)
        sorting = serializers.ChoiceField(required=False, choices=(1, 2, 3))
        genre = serializers.CharField(required=False)
        name = serializers.CharField(required=False)
        author = serializers.CharField(required=False)
        age_category = serializers.ChoiceField(required=False, choices=AGE_CATEGORY)
        views = serializers.IntegerField(required=False, min_value=0)
        avg_rating = serializers.DecimalField(required=False, max_digits=3, 
                                          decimal_places=2,
                                          min_value=0, max_value=5)
        
    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        books = list_books(filters=filters_serializer.validated_data)

        response = get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=BookShortSerializer,
            queryset=books,
            request=request,
            view=self
        )

        return response
    
    
class BookGetApi(APIView):
    class OutputSerializer(BookShortSerializer):

        class Meta:
            model = Book
            fields = ['id', 'name', 'author', 'genres', 
                     'age_category', 'time_created',
                     'time_modified', 'views', 'avg_rating',
                     'slug', 'photo', 'about']
    
    class FilterSerializer(serializers.Serializer):
        from_date = serializers.DateTimeField(required=False)
        to_date = serializers.DateTimeField(required=False)
        sorting = serializers.ChoiceField(required=False, choices=(1, 2, 3))
        genre = serializers.CharField(required=False)
        name = serializers.CharField(required=False)
        author = serializers.CharField(required=False)
        age_category = serializers.ChoiceField(required=False, choices=AGE_CATEGORY)
        views = serializers.IntegerField(required=False, min_value=0)
        avg_rating = serializers.DecimalField(required=False, max_digits=3, 
                                          decimal_places=2,
                                          min_value=0, max_value=5)
        
    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        books = list_books(filters=filters_serializer.validated_data)



        # return response


class CommentListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 3
    
        
    def get(self, request, book_id):
        comments = CommentBook.objects.select_related('user')\
                                      .filter(book=book_id)

        response = get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=CommentSerializer,
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
        
        data = CommentSerializer(comment, context={'request': request}).data
        
        return Response(data)
    
    
class CommentDislikeApi(APIView):
    permission_classes = (IsAuthenticated, )

    
    def get(self, request, comment_id):
        comment = CommentBook.objects.prefetch_related('liked', 'disliked')\
                                     .get(id=comment_id)
        comment = dislike_comment(comment, request.user)
        
        data = CommentSerializer(comment, context={'request': request}).data
        
        return Response(data)


class CommentCreateApi(APIView):
    permission_classes = (IsAuthenticated, )
    
    class InputSerializer(serializers.Serializer):
        body = serializers.CharField()
        book = serializers.IntegerField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        comment = create_comment(request.user,
                                 **serializer.validated_data)
        
        data = CommentSerializer(comment, context={'request': request}).data
        
        return Response(data)


class CommentDeleteApi(APIView):
    permission_classes = (IsAuthenticated, IsAuthor)

    def get(self, request, comment_id):
        comment = get_object_or_404(CommentBook, id=comment_id)
        self.check_object_permissions(self.request, comment)
        comment.delete()
        
        return Response({"deleted": True})
    
    
class BookmarkGetApi(APIView):
    permission_classes = (IsAuthenticated, )
    
    class OutputSerializer(serializers.Serializer):
        bookmarks = serializers.IntegerField()
    
    def get(self, request, book_id):
        relation = get_object_or_404(UserBookRelation, book=book_id,
                                     user=request.user)
        self.check_object_permissions(self.request, relation)
        
        data = self.OutputSerializer(relation).data
        
        return Response(data)
    
    
class BookmarkCreateApi(APIView):
    permission_classes = (IsAuthenticated, )
    
    class InputSerializer(serializers.Serializer):
        bookmarks = serializers.IntegerField()
        book = serializers.IntegerField()
        
    class OutputSerializer(serializers.Serializer):
        bookmarks = serializers.IntegerField(required=False)
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        relation = create_bookmark(**serializer.validated_data, user=request.user)
        
        data = self.OutputSerializer(relation).data
        
        return Response(data)
    

class RatingGetApi(APIView):
    
    class OutputSerializer(serializers.Serializer):
        avg_rating = serializers.FloatField()
    
    def get(self, request, book_id):
        relation = get_average_rating(book_id)
        
        data = self.OutputSerializer(relation).data
        
        return Response(data)
    
    
class RatingCreateApi(APIView):
    permission_classes = (IsAuthenticated, )
    
    class InputSerializer(serializers.Serializer):
        rate = serializers.IntegerField()
        book = serializers.IntegerField()
        
    class OutputSerializer(serializers.Serializer):
        avg_rating = serializers.FloatField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        create_rate(**serializer.validated_data, user=request.user)
        
        relation = get_average_rating(serializer.validated_data['book'])
        
        data = self.OutputSerializer(relation).data
        
        return Response(data)
