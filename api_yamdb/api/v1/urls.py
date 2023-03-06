from django.urls import include, path
from rest_framework import routers

from api.v1.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                          ReviewViewSet, SignupView, TitleViewSet, UserViewSet,
                          YamdbTokenObtainPairView)

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router.register(
    r'users',
    UserViewSet,
    basename='user',
)
router.register(
    'titles',
    TitleViewSet,
    basename='title'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='category'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genre'
)

auth_patterns = [
    path('token/', YamdbTokenObtainPairView.as_view(),
         name='create_token'),
    path('signup/', SignupView.as_view(), name='signup'),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
]
