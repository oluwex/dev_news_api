from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer
)

User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    """
    Register new user.
    """
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]


class UserListAPIView(ListAPIView):
    """
    View all users.
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = UserCreateSerializer
    queryset = User.objects.exclude(is_superuser=True)


class UserDetailAPIView(RetrieveAPIView):
    """
    View a user.
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = UserCreateSerializer
    queryset = User.objects.exclude(is_superuser=True)


class UserLoginAPIView(APIView):
    """
    Authenticates user credentials.
    """
    permission_classes = [AllowAny, ]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,
                            status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)