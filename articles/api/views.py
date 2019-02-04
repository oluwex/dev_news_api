from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    ArticleSerializer,
    ArticleCreateSerializer
)

from ..models import Article
from .permissions import IsAuthor

class ArticleCreateView(CreateAPIView):
    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)


class ArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class ArticleUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor, ]
    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'


class ArticleRetrieveView(RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'


class ArticleDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthor, ]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'
