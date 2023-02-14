from django.urls import include, path
from rest_framework import routers

from api.v1.views import (
    SignupView,
    UsersMeView,
    UserViewSet,
    YamdbTokenObtainPairView,
)

router = routers.DefaultRouter()


urlpatterns = [
    path('auth/token/', YamdbTokenObtainPairView.as_view(),
         name='create_token'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('users/me/', UsersMeView.as_view(), name='me'),
    path('', include(router.urls)),
]
