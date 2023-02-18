from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.permissions import (IsAdminOrReadOnly, IsAdminUser,
                                IsAuthorOrModerAdminPermission)
from api.v1.serializers import (CommentSerializer, ReviewSerializer,
                                SignupSerializer, UserSerializer,
                                UsersMeSerializer,
                                YamdbTokenObtainPairSerializer,
                                TitleSerializer, CategorySerializer,
                                GenreSerializer)
from api.v1.utils import send_confirmation_code
from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User


def get_confirmation_code():
    """Генерирует confirmation_code."""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%&*'
    return get_random_string(20, chars)


def send_confirmation_code(request):
    """Отправляет сгенерированный confirmation_code пользователю."""
    user = get_object_or_404(
        User,
        username=request.data.get('username'),
    )
    user.confirmation_code = get_confirmation_code()
    user.save()
    send_mail(
        'данные для получеия токена',
        f'Код подтверждения {user.confirmation_code}',
        'token@yamdb.ru',
        [request.data.get('email')],
    )


class UserViewSet(ModelViewSet):
    """Вьюсет для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdminUser)


class UsersMeView(APIView):
    """Вью для эндпоинта users/me/."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        me = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        me = get_object_or_404(User, username=request.user.username)
        serializer = UsersMeSerializer(me, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class YamdbTokenObtainPairView(TokenObtainPairView):
    """Вью для получения токена"""
    serializer_class = YamdbTokenObtainPairSerializer


class SignupView(APIView):
    """Вью для регистрации пользователей."""
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            send_confirmation_code(request)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())




class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    #pagination_class = PageNumberPagination

    def get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return get_object_or_404(Review, title = title, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Дженерик для операций retrieve/create/list."""

    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
