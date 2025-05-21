import pytest
import requests

from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
from entities.user import User
from constants.roles import Roles
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture(scope="session")
def requester(session):
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    return CustomRequester(session)


@pytest.fixture(scope="function")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture(scope="function")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        email=SuperAdminCreds.USERNAME,
        password=SuperAdminCreds.PASSWORD,
        roles=list(Roles.SUPER_ADMIN.value),
        api=new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        email=creation_user_data["email"],
        password=creation_user_data["password"],
        roles=list(Roles.USER.value),
        api=new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture(scope="function")
def common_admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_admin = User(
        email=creation_user_data["email"],
        password=creation_user_data["password"],
        roles=list(Roles.ADMIN.value),
        api=new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_admin.api.auth_api.authenticate(common_admin.creds)
    return common_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def test_movie_data():
    """
    Генерация случайного фильма для тестов.
    """
    data = DataGenerator.generate_random_movie()
    return {
        "name": data["name"],
        "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9G",
        "price": data["price"],
        "description": data["description"],
        "location": data["location"],
        "published": data["published"],
        "rating": data["rating"],
        "genreId": data["genreId"],
    }


@pytest.fixture(scope="function")
def test_movie_min_data_item():
    """
    Генерация случайного фильма c минимальным набором обязательных полей для тестов.
    """
    data = DataGenerator.generate_random_movie()
    return {
        "name": data["name"],
        "price": data["price"],
        "description": data["description"],
        "location": data["location"],
        "published": data["published"],
        "genreId": data["genreId"],
    }


@pytest.fixture(scope="function")
def test_movie_negative_data():
    """
    Генерация случайного фильма c минимальным набором обязательных полей для тестов.
    """
    data = DataGenerator.generate_random_movie()
    return {
        "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9G",
        "rating": data["rating"],
    }


@pytest.fixture(scope="function")
def create_movie_for_tests(api_manager, test_movie_data, super_admin):
    """
    Создание фильма для последующих тестов с авторизацией суперюзера.
    """
    # Создаем фильм с использованием авторизованной сессии
    response = super_admin.api.movies_api.create_movie(test_movie_data)

    movie = response.json()
    yield movie

    # Удаляем фильм после тестов
    super_admin.api.movies_api.delete_movie(movie["id"])


@pytest.fixture(scope="function")
def create_movie_for_delete_test(api_manager, test_movie_data, super_admin):
    """
    Создание фильма для DELETE тестов с авторизацией суперюзера.
    """
    # Создаем фильм с использованием авторизованной сессии
    response = super_admin.api.movies_api.create_movie(test_movie_data)

    yield response.json()
