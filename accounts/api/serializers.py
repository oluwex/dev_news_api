from rest_framework.serializers import (
    EmailField,
    CharField,
    ModelSerializer,
    ValidationError
)

from django.contrib.auth import get_user_model

from ..models import Profile

User = get_user_model()


class UserCreateSerializer(ModelSerializer):

    password = CharField(
        label='Password',
        min_length=6,
        write_only=True
    )

    bio = CharField(
        label='Bio',
        min_length=15,
        source='profile.bio'
    )

    name = CharField(label='Name', min_length=10, max_length=40, source='profile.name')

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password',
            'bio'
        ]

    def validate_email(self, value):
        data = self.get_initial()
        email = data['email']
        prev_user = User.objects.filter(email=email)
        if prev_user.exists():
            raise ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        profile = validated_data['profile']
        email = validated_data["email"]
        password = validated_data['password']
        new_user = User(email=email, username=email)
        new_user.set_password(password)
        new_user.save()
        Profile.objects.create(user=new_user, **profile)
        return validated_data