from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(source="avatar.url")
    url = serializers.URLField(source="get_absolute_url")
    
    class Meta:
        model = User
        fields = ['username', 'avatar', 'url']
        
