from rest_framework import status
import pytest
from anees.models import Level
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestRetrieveChild:
    def test_if_user_anonymous_returns_401(self, api_client):
        response = api_client.get("/api/children/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_authenticated_returns_200(self, api_client, authenticate):
        authenticate()
        response = api_client.get("/api/children/me/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_child_created_when_account_created(self, api_client, authenticate):
        authenticate(username="bassiony100")
        response = api_client.get("/api/children/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_info"]["username"] == "bassiony100"

    def test_if_normal_user_cant_view_children_list_returns_403(
        self, api_client, authenticate
    ):
        authenticate()
        response = api_client.get("/api/children/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_can_view_children_list_returns_200(
        self, api_client, authenticate
    ):
        authenticate(is_staff=True)

        response = api_client.get("/api/children/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_can_view_child_detail_returns_200(
        self, api_client, authenticate, create_user
    ):
        authenticate(is_staff=True)
        user = create_user(username="bassiony100", email="test@gmail.com")
        response = api_client.get(f"/api/children/{user.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_info"]["username"] == "bassiony100"

    def test_if_normal_user_cant_view_child_detail_returns_401(
        self, api_client, authenticate, create_user
    ):
        authenticate()
        user = create_user(username="bassiony100", email="beso@gmail.com")

        response = api_client.get(f"/api/children/{user.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_not_found_user_returns_404(self, api_client, authenticate):
        authenticate(is_staff=True)
        response = api_client.get(f"/api/children/100/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_normal_user_can_retrieve_his_words_returns_200(
        self, api_client, authenticate
    ):
        authenticate()

        response = api_client.get("/api/children/me/words/")

        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_can_retreive_any_child_words_returns_200(
        self, api_client, authenticate, create_user
    ):
        authenticate(is_staff=True)
        user = create_user(username="bassiony100", email="beso@gmail.com")
        response = api_client.get(f"/api/children/{user.id}/words/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_child_is_assigned_first_level_on_Create(
        self, api_client, authenticate, create_user, create_levels
    ):
        create_levels()
        authenticate(is_staff=True)

        user = create_user(username="bassiony100", email="beso@gmail.com")
        response = api_client.get(f"/api/children/{user.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_level"] == 1


@pytest.mark.django_db
class TestUpdateChild:
    def test_if_user_can_update_profile_picture_returns_200(
        self, api_client, authenticate, create_img
    ):
        image = create_img()

        authenticate()
        response = api_client.put(
            "/api/children/me/",
            {
                "picture": image,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["picture"] != ""
