from rest_framework import serializers


from .models import CommentBook


class SingleCommentSerializer(serializers.ModelSerializer):
    pass


class OutputReactionSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="comment_likes")
    dislikes = serializers.IntegerField(source="comment_dislikes")
    liked = serializers.SerializerMethodField()
    disliked = serializers.SerializerMethodField()
    
    class Meta:
        model = CommentBook
        fields = ["id", "likes", "dislikes",
                  "liked", "disliked"]
        
    def get_liked(self, obj):
        user = self.context.get('request').user
        return True if user in obj.liked.all() else False
        
    def get_disliked(self, obj):
        user = self.context.get('request').user
        return True if user in obj.disliked.all() else False
