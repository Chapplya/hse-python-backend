from datetime import datetime
from http import HTTPStatus
from faker import Faker
from pydantic import SecretStr
import pytest
from fastapi.testclient import TestClient
import factory
from hw_4.demo_service.api.main import create_app
from hw_4.demo_service.api.utils import initialize
from lecture_4.demo_service.api.contracts import UserResponse
from hw_4.demo_service.core.users import (
    UserInfo,
    UserRole,
    UserService,
    password_is_longer_than_8,
)

app = create_app()


fake = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = dict

    username = factory.Faker("user_name")
    name = factory.Faker("name")
    birthdate = str(fake.date_time().isoformat())
    password = factory.Faker("password")


@pytest.fixture()
def create_user(client):
    resp = client.post("/user-register", json=UserFactory.build(password="12345678910"))
    json = resp.json()
    return UserResponse(
        uid=json["uid"],
        username=json["username"],
        name=json["name"],
        birthdate=json["birthdate"],
        role=json["role"],
    )


@pytest.fixture()
def client():
    with TestClient(app) as client:
        user_service = UserService(password_validators=[password_is_longer_than_8])
        user_service.register(
            UserInfo(
                username="kaban",
                name="papa",
                birthdate=datetime(2001, 12, 10),
                role=UserRole.ADMIN,
                password=SecretStr("123456789"),
            )
        )
        app.state.user_service = user_service

        yield client

        if hasattr(app.state, "user_service"):
            app.state.user_service._data.clear()
            app.state.user_service._username_index.clear()
            app.state.user_service._last_id = 0


def test_correct_register(client):
    response = client.post(
        "/user-register", json=UserFactory.build(password="1234567890")
    )
    assert response.status_code == HTTPStatus.OK


def test_fail_register_usename(client):
    response = client.post(
        "/user-register",
        json=UserFactory.build(password="123"),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_by_username(client):
    response = client.post("/user-get", params={"id": 1}, auth=("kaban", "123456789"))

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["uid"] == 1
    assert data["username"] == "kaban"
    assert data["name"] == "papa"
    assert data["role"] == "admin"


@pytest.mark.parametrize(
    "parameters,auth_name, auth_passw, excpected_code",
    [
        (
            {"id": 10, "username": "test_user"},
            "kaban",
            "123456789",
            HTTPStatus.BAD_REQUEST,
        ),
        ({}, "kaban", "123456789", HTTPStatus.BAD_REQUEST),
        ({"username": "unnreal_name"}, "kaban", "123456789", HTTPStatus.NOT_FOUND),
        ({"id": 1}, "kaban", "12345678900", HTTPStatus.UNAUTHORIZED),
    ],
)
def test_error_none_params_user_get(
    client, parameters, auth_name, auth_passw, excpected_code
):
    response = client.post("/user-get", params=parameters, auth=(auth_name, auth_passw))

    assert response.status_code == excpected_code


def test_get_usename(client):
    response = client.post(
        "/user-get", params={"username": "kaban"}, auth=("kaban", "123456789")
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data == {
        "uid": 1,
        "username": "kaban",
        "name": "papa",
        "role": "admin",
        "birthdate": "2001-12-10T00:00:00",
    }


@pytest.mark.parametrize(
    "param, excepted_code",
    [({"id": 1}, HTTPStatus.OK), ({"id": 52}, HTTPStatus.BAD_REQUEST)],
)
def test_user_promote(client, param, excepted_code):
    response = client.post(
        "/user-promote",
        params=param,
        auth=("kaban", "123456789"),
    )
    assert response.status_code == excepted_code


def test_fail_403_promote_user_without_admin(client, create_user):
    user = create_user
    response = client.post(
        "/user-promote",
        params={"id": user.uid},
        auth=(user.username, "12345678910"),
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_initialize():
    app = create_app()
    async with initialize(app):
        user_service = app.state.user_service
        admin = user_service.get_by_username("admin")
        expected_data = {
            "uid": 1,
            "info": {
                "username": "admin",
                "name": "admin",
                "role": "admin",
                "password": str(SecretStr("superSecretAdminPassword123")),
                "birthdate": "1970-01-01T03:00:00",
            },
        }

        admin_data = admin.model_dump(mode="json")

        assert admin_data == expected_data
