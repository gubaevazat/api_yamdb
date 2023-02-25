from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializerGet(serializers.ModelSerializer):
    # category = SlugRelatedField(slug_field='name', read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    # def create(self, validated_data):
    #     if 'category' not in self.initial_data:
    #         title = Title.objects.create(**validated_data)
    #         return title
    #     categories = validated_data.pop('category')
    #     title = Title.objects.create(**validated_data)

    #     for category in categories:
    #         current_category, status = Category.objects.get_or_create(**category)
    #     return title

    # def create(self, validated_data):
    #     if 'category' not in self.initial_data:
    #         title = Title.objects.create(**validated_data)
    #         return title
    #     category = validated_data.pop('category')
    #     title = Title.objects.create(**validated_data)
    #     return title


class TitleSerializerPost(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name', read_only=True)
    # genre = GenreSerializer(read_only=True, many=True)
    # category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    # def create(self, validated_data):
    #     if 'category' not in self.initial_data:
    #         title = Title.objects.create(**validated_data)
    #         return title
    #     category = validated_data.pop('category')
    #     title = Title.objects.create(**validated_data)
    #     return title


class CurrentTitle(object):

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs['title_id']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=CurrentTitle()
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Автор может оставить только один отзыв!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
