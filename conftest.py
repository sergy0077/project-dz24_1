import pytest
from model_bakery import baker
from rest_framework.test import APIClient

@pytest.fixture
def user():
    user = baker.make_recipe('users.User')
    user.set_password("password123")
    return user

@pytest.fixture
def client():
    client = APIClient()
    return client