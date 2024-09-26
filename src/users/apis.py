from rest_framework import serializers
from rest_framework.views import APIView

from api.pagination import get_paginated_response, LimitOffsetPagination

from books.models import CommentBook
from books.serializers import CommentSerializer, BookShortSerializer


class UserCommentListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100
        
    class OutputSerializer(CommentSerializer):
        book = BookShortSerializer()
        
        class Meta:
            model = CommentBook
            fields = ["id", "likes", "dislikes",
                     "liked", "disliked", "time_created",
                     "user", "body", "is_creator", "book"]
                
    def get(self, request, user_id: int):
        comments = CommentBook.objects.filter(user=user_id)\
                                      .order_by('-time_created')
        
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=comments,
            request=request,
            view=self
        )
