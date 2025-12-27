from rest_framework import status
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

User = get_user_model()


@pytest.mark.django_db
class TestCreateUser:
    def test_if_user_register_returns_201_created(self, api_client):
        user = {
            "first_name": "Mahmoud",
            "last_name": "Bassiony",
            "username": "bassiony17",
            "gender": "M",
            "date_of_birth": "2000-01-01",
            "email": "beso.beso2468@gmail.com",
            "password": "backendisnotfunny",
            "re_password": "backendisnotfunny",
        }
        response = api_client.post("/auth/users/", user)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == user["email"]
        assert response.data["id"] > 0

    def test_if_missing_field_when_resistering_returns_400_bad_request(
        self, api_client
    ):
        user = {
            "first_name": "Mahmoud",
            "last_name": "Bassiony",
        }
        response = api_client.post("/auth/users/", user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveUser:
    def test_if_user_anynoumous_returns_401_unauthorized(self, api_client):
        response = api_client.get("/auth/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_normal_user_access_user_list_returns_404_not_found(
        self, api_client, authenticate
    ):
        authenticate()
        response = api_client.get("/auth/users/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_admin_access_user_list_returns_200_ok(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.get("/auth/users/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_normal_user_access_profile_returns_200_ok(
        self, api_client, authenticate
    ):
        authenticate()
        response = api_client.get("/auth/users/me/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_normal_user_access_other_user_profile_returns_404_not_found(
        self, api_client, authenticate
    ):
        authenticate()
        user = baker.make(User)
        response = api_client.get(f"/auth/users/{user.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_admin_access_any_profile_returns_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        user = baker.make(User)
        response = api_client.get(f"/auth/users/{user.id}/")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUpdateUser:
    def test_if_user_missing_fields_when_updating_all_data_return_400(
        self, api_client, authenticate
    ):
        authenticate()
        response = api_client.put(f"/auth/users/me/", {"first_name": "Mahmoud"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_updating_all_data_returns_200(self, api_client, authenticate):
        authenticate()
        response = api_client.put(
            f"/auth/users/me/",
            {
                "first_name": "Mahmoud",
                "last_name": "Bassiony",
                "date_of_birth": "2023-07-05",
                "gender": "M",
                "email": "b.eso.beso.2468@gmail.com",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Mahmoud"
        assert response.data["last_name"] == "Bassiony"
        assert response.data["date_of_birth"] == "2023-07-05"

    def test_if_user_updating_patrial_data_returns_200(self, api_client, authenticate):
        authenticate()
        response = api_client.patch(
            f"/auth/users/me/",
            {
                "first_name": "Mahmoud",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Mahmoud"

    def test_if_admin_can_update_any_profile_returns_200(
        self, api_client, authenticate
    ):
        authenticate(is_staff=True)
        user = baker.make(User)
        response = api_client.patch(
            f"/auth/users/{user.id}/",
            {
                "first_name": "Mahmoud",
            },
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteUser:
    def test_if_user_delete_his_profile_returns_204(self, api_client, authenticate):
        authenticate()
        response = api_client.delete(
            "/auth/users/me/", {"current_password": "backendisnotfunny"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_admin_cant_delete_any_profile_returns_204(
        self, api_client, authenticate, create_user
    ):
        authenticate(is_staff=True)
        user = create_user(username="bassiony18", email="test@gmail.com")
        response = api_client.delete(f"/auth/users/{user.id}/")
        assert response.status_code != status.HTTP_204_NO_CONTENT
