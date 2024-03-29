import decimal

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken

from api.v1.utils import CurrentTitle
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_year
from user.models import User
from user.validators import validate_username


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

    username = serializers.CharField(
        max_length=150,
        validators=(
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        )
    )

    class Meta:
        fields = ('username', 'email')
        model = User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializerGet(serializers.ModelSerializer):
    """Сериализатор произведений для операций чтения."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.DecimalField(
        read_only=True,
        max_digits=3,
        decimal_places=1,
        coerce_to_string=False,
        rounding=decimal.ROUND_HALF_DOWN,
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class TitleSerializerPost(serializers.ModelSerializer):
    """Сериализатор произведений для операций создания-редактирования."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )
    year = serializers.IntegerField(
        validators=(validate_year,)
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

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
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
