from django.urls import include, path
from rest_framework import routers

from api.v1.views import (
    ReviewViewSet,
    CommentViewSet,
    SignupView,
    UsersMeView,
    UserViewSet,
    YamdbTokenObtainPairView,
)

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

urlpatterns = [
    path('auth/token/', YamdbTokenObtainPairView.as_view(),
         name='create_token'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('users/me/', UsersMeView.as_view(), name='me'),
    path('', include(router.urls)),
]
