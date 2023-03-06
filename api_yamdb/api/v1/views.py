from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.filters import TitleFilter
from api.v1.mixins import CreateListDestroyViewSet
from api.v1.permissions import (IsAdminOrReadOnly, IsAdminUser,
                                IsAuthorOrModerAdminPermission)
from api.v1.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, ReviewSerializer,
                                SignupSerializer, TitleSerializerGet,
                                TitleSerializerPost, UserSerializer,
                                UsersMeSerializer,
                                YamdbTokenObtainPairSerializer)
from api.v1.utils import send_confirmation_code
from reviews.models import Category, Genre, Review, Title
from user.models import User


class UserViewSet(ModelViewSet):
    """Вьюсет для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdminUser)

    @action(detail=False, methods=['get', 'patch'], url_path='me', permission_classes = (IsAuthenticated,))
    def me(self, request):
        if request.method == "GET":
            me = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(me)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            me = get_object_or_404(User, username=request.user.username)
            serializer = UsersMeSerializer(me, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class YamdbTokenObtainPairView(TokenObtainPairView):
    """Вью для получения токена."""
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
    """Вьюсет для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModerAdminPermission)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModerAdminPermission)

    def get_review(self):
        return get_object_or_404(
            Review,
            title=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleSerializerGet
        return TitleSerializerPost


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
