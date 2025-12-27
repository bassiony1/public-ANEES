from rest_framework.test import APIClient
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
from anees.models import (
    Level,
    Receptive,
    ReceptiveImage,
    Expressive,
    Social,
    conversionMessage,
)

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
    def _authenticate(
        is_staff=False, username="bassiony17", email="bassiony@gmail.com"
    ):
        user = create_user(username=username, email=email)
        user.is_staff = is_staff
        return api_client.force_authenticate(user=user)

    return _authenticate


@pytest.fixture
def create_levels(create_level):
    def _create_levels():
        create_level(1)
        create_level(2)
        create_level(3)
        create_level(4)

    return _create_levels


@pytest.fixture
def create_level(create_receptive_game, create_expressive_game, create_social_game):
    def _create_level(level_num):
        lev = Level.objects.create(level_num=level_num)
        create_receptive_game(lev)
        create_expressive_game(lev)
        create_social_game(lev)
        return lev

    return _create_level


@pytest.fixture
def create_img():
    def _create_img():
        return SimpleUploadedFile(
            name="test_image.png",
            content=open("anees/tests/test.png", "rb").read(),
            content_type="image/png",
        )

    return _create_img


@pytest.fixture
def create_receptive_game(create_img):
    def _create_receptive_game(level_num):
        rec = Receptive.objects.create(answer="test4", level=level_num)
        ReceptiveImage.objects.create(img=create_img(), name="test1", receptive=rec)
        ReceptiveImage.objects.create(img=create_img(), name="test2", receptive=rec)
        ReceptiveImage.objects.create(img=create_img(), name="test3", receptive=rec)
        ReceptiveImage.objects.create(img=create_img(), name="test4", receptive=rec)
        return rec

    return _create_receptive_game


@pytest.fixture
def create_expressive_game(create_img):
    def _create_expressive_game(level_num):
        exp = Expressive.objects.create(
            answer="test", level=level_num, img=create_img()
        )

        return exp

    return _create_expressive_game


@pytest.fixture
def create_social_game(create_img):
    def _create_social_game(level_num):
        soc = Social.objects.create(video=create_img(), level=level_num)
        conversionMessage.objects.create(message="test1", social=soc)
        conversionMessage.objects.create(message="test2", social=soc)
        conversionMessage.objects.create(message="test3", social=soc)
        conversionMessage.objects.create(message="test4", social=soc)

        return soc

    return _create_social_game
