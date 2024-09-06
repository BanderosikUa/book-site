from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(source="avatar.url")
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['username', 'avatar', 'url']
        
    def get_url(self, obj):
        return obj.get_absolute_url
