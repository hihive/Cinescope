from api.api_manager import ApiManager
from conftest import test_movie_data
from constants.constants import SUPERUSER, INVALID_MOVIE_ID


def auth_superuser(api_manager: ApiManager):
    api_manager.auth_api.authenticate(SUPERUSER)


class TestMoviesAPI:
    # VALID TESTS
    def test_get_movies(self, api_manager: ApiManager):
        """
        Тест на получение информации о фильмах
        """
        # Получение полного списка фильмов без фильтров
        response = api_manager.movies_api.get_movies()

        # Проверка, что фильмы есть в базе
        assert isinstance(response.json()["movies"], list)

    def test_get_movies_with_params(self, api_manager: ApiManager):
        """
        Тест на получение информации о фильмах с фильтром
        """
        # Получение списка фильмов c фильтром
        params = {"minPrice": 10, "maxPrice": 50}
        response = api_manager.movies_api.get_movies(params)

        response_data = response.json()
        # Проверка на соответствие фильтру
        for movie in response_data["movies"]:
            assert (params["minPrice"] < movie["price"] < params["maxPrice"]), "Ошибка фильтрации"

    def test_get_movie(self, api_manager: ApiManager, create_movie_for_tests):
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

    # INVALID TESTS
    def test_get_invalid_movie(self, api_manager: ApiManager, create_movie_for_tests):
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

    def test_create_movie_with_unauthorization_user(self, api_manager: ApiManager, test_movie_data):
        """
        Тест на создание фильма незарегистрированным пользователем
        """
        # Проверка создания фильма с незарегистрированным пользователем
        api_manager.movies_api.create_movie(test_movie_data, expected_status=401)

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
