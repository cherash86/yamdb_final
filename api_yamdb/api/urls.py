from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views
from users.views import signup, token, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'titles', views.TitleViewSet, basename='titles')
router_v1.register(
    r'categories',
    views.CategoryViewSet,
    basename='categories'
)
router_v1.register(r'genres', views.GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', token),
    path('v1/', include(router_v1.urls)),
]
