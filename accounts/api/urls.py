from django.urls import path

from .views import UserCreateAPIView, UserListAPIView, UserLoginAPIView, UserDetailAPIView

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('authors/', UserListAPIView.as_view(), name='users'),
    path('authors/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('author/register/', UserCreateAPIView.as_view(), name='register'),
]