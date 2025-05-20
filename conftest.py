import pytest
import requests

from constants import SUPERUSER
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
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


@pytest.fixture(scope="session")
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
        "roles": ["USER"],
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
def create_movie_for_tests(api_manager, test_movie_data):
    """
    Создание фильма для последующих тестов с авторизацией суперюзера.
    """
    # Выполняем авторизацию суперюзера через api_manager
    api_manager.auth_api.authenticate(SUPERUSER)

    # Создаем фильм с использованием авторизованной сессии
    response = api_manager.movies_api.create_movie(test_movie_data)

    movie = response.json()
    yield movie

    # Удаляем фильм после тестов
    api_manager.movies_api.delete_movie(movie["id"])
    # Аутентификация суперюзер
    api_manager.auth_api.logout()


@pytest.fixture(scope="function")
def create_movie_for_delete_test(api_manager, test_movie_data):
    """
    Создание фильма для DELETE тестов с авторизацией суперюзера.
    """
    # Выполняем авторизацию суперюзера через api_manager
    api_manager.auth_api.authenticate(SUPERUSER)

    # Создаем фильм с использованием авторизованной сессии
    response = api_manager.movies_api.create_movie(test_movie_data)

    movie = response.json()
    yield movie

    # Аутентификация суперюзер
    api_manager.auth_api.logout()
