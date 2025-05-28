import datetime
from datetime import timezone
from http.cookiejar import UTC_ZONES
from venv import logger

import pytest

from conftest import test_movie_data, common_user, common_admin, super_admin
from constants.constants import INVALID_MOVIE_ID
from models.base_models import MovieDBModel
from utils.data_generator import DataGenerator


class TestMoviesAPI:
    # VALID TESTS
    def test_get_movies(self, api_manager):
        """
        Тест на получение информации о фильмах
        """
        # Получение полного списка фильмов без фильтров
        response = api_manager.movies_api.get_movies()

        # Проверка, что фильмы есть в базе
        assert isinstance(response.json()["movies"], list)

    @pytest.mark.parametrize("params", [
        {"minPrice": 10, "maxPrice": 50, "genreId": 1},
        {"minPrice": 100, "maxPrice": 200, "genreId": 3}
    ])
    def test_get_movies_with_params(self, api_manager, params):
        """
        Тест на получение информации о фильмах с фильтром
        """
        # Получение списка фильмов c фильтром
        response = api_manager.movies_api.get_movies(params)

        response_data = response.json()
        # Проверка на соответствие фильтру
        for movie in response_data["movies"]:
            assert (params["minPrice"] < movie["price"] < params["maxPrice"]), "Ошибка фильтрации по полю price"
            assert movie["genreId"] == params["genreId"], "Ошибка фильтрации по полю genreId"

    def test_get_movie(self, api_manager, create_movie_for_tests):
        """
        Тест на получение информации о фильме
        """
        # Создаю фильм, чтобы получить его id
        movie = create_movie_for_tests

        # Проверка получения фильма с валидным ID
        api_manager.movies_api.get_movie(movie["id"])

    def test_create_movie(self, test_movie_data, super_admin):
        """
        Тест на создание фильма
        """
        # Проверка создания фильма с валидными данными
        super_admin.api.movies_api.create_movie(test_movie_data)

    def test_create_movie_with_min_data_item(self, test_movie_min_data_item, super_admin):
        """
        Тест на создание фильма только с обязательными полями
        """
        # Проверка создания фильма с минимальным набором обязательных полей
        super_admin.api.movies_api.create_movie(test_movie_min_data_item)

    def test_update_movie(self, test_movie_data, create_movie_for_tests, super_admin):
        """
        Тест на обновление фильма
        """
        # Создаю фильм, чтобы получить его id
        movie = create_movie_for_tests

        # Успешное обновление фильма с валидным ID
        super_admin.api.movies_api.update_movie(movie["id"], test_movie_data)

    def test_delete_movie(self, create_movie_for_delete_test, super_admin):
        """
        Тест на удаление информации о фильме
        """
        # Создаю фильм, чтобы получить его id
        movie = create_movie_for_delete_test
        movie_id = movie["id"]

        # Успешное удаление фильма с валидным ID
        super_admin.api.movies_api.delete_movie(movie_id)

        # Проверка, что фильм больше не доступен
        super_admin.api.movies_api.get_movie(movie_id, expected_status=404)


    @pytest.mark.slow
    @pytest.mark.parametrize("user,expected_status", [
        ("common_user", 403),
        ("common_admin", 403),
        ("super_admin", 200)
    ], ids=["User", "Admin", "SuperAdmin"])
    def test_delete_movie_all_users(self, super_admin, create_movie_for_delete_test, user, expected_status, request):
        """
        Тест на удаление фильмов всеми видами пользователей
        """
        # Активирую фикстуры переданные через parametrize
        user_fixture = request.getfixturevalue(user)

        # Создаю фильм, чтобы получить его id
        movie = create_movie_for_delete_test
        movie_id = movie["id"]

        # Удаление фильма с валидным ID
        user_fixture.api.movies_api.delete_movie(movie_id, expected_status=expected_status)

        # Чистка после пользователей у которых нет прав на удаление фильмов
        if expected_status == 403:
            super_admin.api.movies_api.delete_movie(movie_id)

        # Проверяю, что фильм действительно был удален
        user_fixture.api.movies_api.get_movie(movie_id, expected_status=404)

    # INVALID TESTS
    @pytest.mark.slow
    def test_get_invalid_movie(self, api_manager, create_movie_for_tests):
        """
        Тест на получение информации о фильме по несуществующему id
        """
        # Проверка получения фильма с невалидным ID
        api_manager.movies_api.get_movie(INVALID_MOVIE_ID, expected_status=404)

    def test_create_invalid_movie(self, super_admin, test_movie_negative_data):
        """
        Тест на создание фильма без обязательных полей
        """
        # Проверка создания фильма с отсутствием обязательных полей
        super_admin.api.movies_api.create_movie(test_movie_negative_data, expected_status=400)

    def test_create_movie_with_unauthorization_user(self, api_manager, test_movie_data):
        """
        Тест на создание фильма незарегистрированным пользователем
        """
        # Проверка создания фильма с незарегистрированным пользователем
        api_manager.movies_api.create_movie(test_movie_data, expected_status=401)

    @pytest.mark.slow
    def test_create_movie_without_access_user(self, common_admin, test_movie_data):
        """
        Тест на создание фильма пользователем без прав доступа
        """
        # Проверка создания фильма с пользователем без прав доступа
        common_admin.api.movies_api.create_movie(test_movie_data, expected_status=403)

    def test_update_invalid_movie(self, super_admin, test_movie_data):
        """
        Тест на обновление несуществующего фильма
        """
        # Изменение фильма с невалидным ID
        super_admin.api.movies_api.update_movie(INVALID_MOVIE_ID, test_movie_data, expected_status=404)

    def test_delete_invalid_movie(self, super_admin):
        """
        Тест на удаление несуществующего фильма
        """
        # Удаление фильма с невалидным ID
        super_admin.api.movies_api.delete_movie(INVALID_MOVIE_ID, expected_status=404)

    def test_create_delete_movie(self, super_admin, db_session):
        """
        Тест на проверку работы БД при создании и удалении фильма
        """

        # Подготовка тестовых данных
        movie = DataGenerator.generate_random_movie()

        # Проверка, что на данный момент такого фильма нет в БД
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie["name"])
        assert movies_from_db.count() == 0, "В базе уже присутствует фильм с таким названием"

        # Создаю фильм
        response = super_admin.api.movies_api.create_movie(movies_data=movie)
        assert response.status_code == 201, "Фильм должен успешно создаться"
        response = response.json()


        # Проверка
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == response["name"])
        assert movies_from_db.one(), "В базе уже присутствует фильм с таким названием"

        movie_from_db = movies_from_db.first()

        # Проверка что сервис заполнил верно created_at с погрешностью в 5 минут
        assert movie_from_db.created_at >= (
                datetime.datetime.now(timezone.utc).replace(tzinfo=None) - datetime.timedelta(
            minutes=5)), "Сервис выставил время создания с большой погрешностью"

        # Удаляем фильм из базы данных
        super_admin.api.movies_api.delete_movie(movie_id=response["id"])


        # проверяем что в конце тестирования фильма с таким названием действительно нет в базе
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
        assert movies_from_db.count() == 0, "Фильм небыл удален из базы!"


