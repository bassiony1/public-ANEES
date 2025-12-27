from rest_framework.test import APIClient
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(username="bassiony17", email="bassiony@gmail.com"):
        return User.objects.create_user(
            username=username,
            email=email,
            gender="M",
            date_of_birth="2000-01-01",
            first_name="Mahmoud",
            last_name="Bassiony",
            password="backendisnotfunny",
        )

    return _create_user


@pytest.fixture
def authenticate(api_client, create_user):
    def _authenticate(is_staff=False):
        user = create_user()
        user.is_staff = is_staff
        return api_client.force_authenticate(user=user)

    return _authenticate
