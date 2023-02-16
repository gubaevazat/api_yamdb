from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
