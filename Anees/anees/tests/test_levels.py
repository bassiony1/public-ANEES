from rest_framework import status
import pytest
from anees.models import Level
from model_bakery import baker


@pytest.mark.django_db
class TestRetrieveLevels:
    def test_if_user_anonymous_returns_401(self, api_client):
        response = api_client.get("/api/levels/")
        print(response.status_code)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_authenticated_returns_200(self, api_client, authenticate):
        authenticate()
        response = api_client.get("/api/levels/")
        print(response.status_code)
        assert response.status_code == status.HTTP_200_OK

    def test_if_level_exists_returns_200(self, api_client, authenticate):
        authenticate()
        level = baker.make(Level, level_num=1)
        response = api_client.get("/api/levels/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["level_num"] == level.level_num

    def test_if_level_does_not_exist_returns_404(self, api_client, authenticate):
        authenticate()
        response = api_client.get("/api/levels/16/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_level_contains_at_least_one_game(
        self, api_client, authenticate, create_level
    ):
        authenticate()
        create_level(1)

        response = api_client.get("/api/levels/1/receptive/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_child_can_clear_game(self, api_client, authenticate, create_levels):
        authenticate()
        create_levels()

        response = api_client.post("/api/levels/1/receptive/", {"score": 100})
        assert response.status_code == status.HTTP_200_OK
        response = api_client.get("/api/levels/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["receptive_score"] == 100
        assert response.data["receptive_complete"] == True

    def test_if_child_can_clear_level(self, api_client, authenticate, create_levels):
        create_levels()
        authenticate()
        response = api_client.get("/api/levels/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        api_client.post("/api/levels/1/receptive/", {"score": 100})
        api_client.post("/api/levels/1/expressive/", {"score": 100})
        api_client.post("/api/levels/1/social/", {"score": 100})

        response = api_client.get("/api/levels/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_if_child_can_not_clear_level_without_clear_all_games(
        self, api_client, authenticate, create_levels
    ):
        create_levels()
        authenticate()
        response = api_client.get("/api/levels/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        api_client.post("/api/levels/1/receptive/", {"score": 100})
        api_client.post("/api/levels/1/expressive/", {"score": 100})

        response = api_client.get("/api/levels/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_if_score_gets_updated_to_high_score(
        self, api_client, authenticate, create_levels
    ):
        create_levels()
        authenticate()
        api_client.post("/api/levels/1/receptive/", {"score": 80})
        api_client.post("/api/levels/1/receptive/", {"score": 100})

        response = api_client.get("/api/levels/1/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["receptive_score"] == 100
