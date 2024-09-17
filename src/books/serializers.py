from rest_framework import serializers

from users.serializers import UserSerializer


from .models import CommentBook


class SingleCommentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context['request'].user if 'request' in self.context else None
    
    user = UserSerializer()
    comment = serializers.CharField(source="body")
    likes = serializers.IntegerField(source="comment_likes")
    dislikes = serializers.IntegerField(source="comment_dislikes")
    liked = serializers.SerializerMethodField()
    disliked = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()
    
    class Meta:
        model = CommentBook
        fields = ["id", "likes", "dislikes",
                  "liked", "disliked", "time_created",
                  "user", "is_creator", "comment"]
        
    def get_liked(self, obj):
        return True if self.user in obj.liked.all() else False
        
    def get_disliked(self, obj):
        return True if self.user in obj.disliked.all() else False
    
    def get_is_creator(self, obj):
        return obj.user == self.user
