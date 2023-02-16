import re

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class UsersMeSerializer(UserSerializer):
    """Сериализатор для эндпоинта users/me/."""

    role = serializers.CharField(read_only=True)


class YamdbTokenObtainPairSerializer(serializers.Serializer):
    """Сериализатор получения токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=20)

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError('Не верный confirmation_code')
        return {'access': str(AccessToken.for_user(user))}


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'me нельзя использовать в качестве имени',
            )
        return value

    class Meta:
        fields = ('username', 'email')
        model = User
        

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment