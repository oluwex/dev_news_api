from django.urls import path

from .views import ArticleCreateView, ArticleRetrieveView, ArticleUpdateView, ArticleListView, ArticleDeleteView

app_name = 'articles-api'

urlpatterns = [
    path('', ArticleListView.as_view(), name='view_articles'),
    path('create/', ArticleCreateView.as_view(), name='create_article'),
    path('<str:slug>/', ArticleRetrieveView.as_view(), name='retrieve_article'),
    path('<str:slug>/update/', ArticleUpdateView.as_view(), name='update_article'),
    path('<str:slug>/delete/', ArticleDeleteView.as_view(), name='delete_article'),
]