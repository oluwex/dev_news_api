from django.urls import path

from .views import UserCreateAPIView, UserListAPIView

app_name = 'accounts'

urlpatterns = [
    path('authors/register/', UserCreateAPIView.as_view(), name='register'),
    path('authors/', UserListAPIView.as_view(), name='users'),
]