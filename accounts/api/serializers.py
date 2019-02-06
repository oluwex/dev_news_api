from rest_framework.serializers import (
    EmailField,
    CharField,
    HyperlinkedIdentityField,

    ModelSerializer,
    ValidationError
)
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

from ..models import Profile

User = get_user_model()


class UserCreateSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(
        view_name="accounts-api:user-detail",
        lookup_field='pk'
    )

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
            'url',
            'name',
            'email',
            'password',
            'bio'
        ]
        extra_kwargs = {'email': {'required': True}}

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


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label='Email address', required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        password = data["password"]

        user = User.objects.filter(email=email)
        if user.exists():
            user_obj = user.first()
        else:
            raise ValidationError("Incorrect credentials. Please try again.")

        if not user_obj.check_password(password):
            raise ValidationError("Incorrect credentials. Please try again.")

        try:
            data['token'] = Token.objects.get(user=user_obj)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user_obj)
            data['token'] = token.key

        return data