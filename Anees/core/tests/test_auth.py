from rest_framework import status
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthentication:
    def test_if_user_login_with_correct_credentials_returns_200(
        self, api_client, create_user
    ):
        user = create_user()

        response = api_client.post(
            "/auth/jwt/create/",
            {
                "username": user.username,
                "password": "backendisnotfunny",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"] is not None
        assert response.data["refresh"] is not None

    def test_if_user_login_with_bad_credentials_returns_401(
        self, api_client, create_user
    ):
        user = create_user()
        response = api_client.post(
            "/auth/jwt/create/",
            {
                "username": user.username,
                "password": "backendisfunny",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_can_refresh_access_token_returns_200(
        self, api_client, create_user
    ):
        user = create_user()
        response = api_client.post(
            "/auth/jwt/create/",
            {
                "username": user.username,
                "password": "backendisnotfunny",
            },
        )
        refresh_token = response.data["refresh"]
        response = api_client.post(
            "/auth/jwt/refresh/",
            {
                "refresh": refresh_token,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"] is not None
