from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, ListAPIView

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
)

from .serializers import (
    UserCreateSerializer
)

User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]


class UserListAPIView(ListAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.exclude(is_superuser=True)