from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import filters, mixins, permissions
from django_filters.rest_framework import DjangoFilterBackend
from reviews import models
from django.db.models import Avg
from users.permissions import Admin, Superuser, ReadOnly
from users.permissions import IsAdminAuthorOrReadOnlyPermission
from . import serializers
from .utils import TitleFilter


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               GenericViewSet):
    pass


class TitleViewSet(ModelViewSet):
    """Получить список всех произведений, изменить и добавить их."""
    queryset = models.Title.objects.annotate(
        rating=Avg("reviews__score")).all()
    permission_classes = [Admin | Superuser | ReadOnly]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitleSafeSerializer
        return serializers.TitleCreatePatchDeleteSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """Получить список всех категорий, изменить и добавить их."""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [Admin | Superuser | ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(ListCreateDestroyViewSet):
    """Получить список всех жанров, изменить и добавить их."""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [Admin | Superuser | ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAdminAuthorOrReadOnlyPermission, ]

    def get_title(self):
        return get_object_or_404(models.Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAdminAuthorOrReadOnlyPermission, ]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(models.Review, id=review_id,
                                 title_id=title_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
