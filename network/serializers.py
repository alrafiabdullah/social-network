from rest_framework import serializers
from .models import Post, Like, User, Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'post_owner',
            'text_field',
            'post_time',
            'is_edited',
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'liked_by', 'liked_post')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'user', 'user_following', 'user_follower')
