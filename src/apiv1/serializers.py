from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from Books.models import Book, CommentBook
from Books.models import UserBookRelation
from Genres.models import Genre
from users.models import Profile, CustomUser


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'bookmarks', 'rate')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('author_is_user', 'slug', 'readers')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('slug', )


class BookListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Book
        fields = ('name', 'id', 'photo',
                  'author', 'genre', 'time_created', 'url')


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_user_avatar')
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'avatar', 'url',
                  'username')

    def get_user_avatar(self, obj):
        return obj.avatar.url



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class CommentBookSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField('get_likes_count')
    dislikes = serializers.SerializerMethodField('get_dislikes_count')
    user = UserSerializer(required=False, default=serializers.CurrentUserDefault())
    user_is_creator = serializers.SerializerMethodField('get_user_is_creator')

    class Meta:
        model = CommentBook
        exclude = ('liked', 'disliked',)

    def get_likes_count(self, obj):
        return obj.liked.all().count()

    def get_dislikes_count(self, obj):
        return obj.disliked.all().count()

    def get_user_is_creator(self, obj):
        print(self.context['request'].user)
        return obj.user == self.context['request'].user
