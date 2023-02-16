from django.urls import include, path
from rest_framework import routers
from api.v1.views import CommentViewSet, ReviewViewSet

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



urlpatterns = [
    path('', include(router.urls))
]
