from rest_framework import serializers

from users.serializers import UserSerializer


from .models import CommentBook, Book


class CommentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context['request'].user if 'request' in self.context else None
    
    user = UserSerializer()
    body = serializers.CharField()
    likes = serializers.IntegerField(source="comment_likes")
    dislikes = serializers.IntegerField(source="comment_dislikes")
    liked = serializers.SerializerMethodField()
    disliked = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()
    
    class Meta:
        model = CommentBook
        fields = ["id", "likes", "dislikes",
                  "liked", "disliked", "time_created",
                  "user", "body", "is_creator"]
        
    def get_liked(self, obj):
        return True if self.user in obj.liked.all() else False
        
    def get_disliked(self, obj):
        return True if self.user in obj.disliked.all() else False
    
    def get_is_creator(self, obj):
        return obj.user == self.user


class BookShortSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    url = serializers.URLField(source="get_absolute_url")
    
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'genres', 
                  'age_category', 'time_created',
                  'time_modified', 'views', 'avg_rating',
                  'slug', 'photo', 'url']
        # abstract=True
        
    def get_author(self, obj):
        if obj.author:
            return obj.author.name
        else:
            return None
    
    def get_genres(self, obj):
        return list(obj.genre.values_list("name", flat=True))
    
    def get_views(self, obj):
        return obj.hit_count.hits
    
    def get_avg_rating(self, obj):
        if hasattr(obj, "avg_rating"):
            return obj.avg_rating
