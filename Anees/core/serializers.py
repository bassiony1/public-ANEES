from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer,
    UserSerializer as BaseUserUpdateSerializer,
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer,
)
from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.conf import settings
from anees.models import Child, ChildLevel, Level

User = get_user_model()


class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "password",
        ]


class UserUpdateSerializer(BaseUserUpdateSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "date_of_birth", "gender"]
