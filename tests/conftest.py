import pytest
from src.api.pet_api import PetApi
from src.http.client import HttpClient


@pytest.fixture
def http_client():
    return HttpClient()


@pytest.fixture
def pet_api(http_client):
    return PetApi(http_client)

