from api.api_manager import ApiManager
from constants import SUPERUSER


def auth_superuser(api_manager: ApiManager):
    api_manager.auth_api.authenticate(SUPERUSER)


class TestMoviesAPI:
    def test_get_movies(self, api_manager: ApiManager):
        """
        Тест на получение информации о фильмах
        """
        # Получение полного списка фильмов без фильтров
        response = api_manager.movies_api.get_movies()
        assert isinstance(response.json()["movies"], list)

        # Получение списка фильмов по фильтру
        params = {"minPrice": 10, "maxPrice": 50}
        response = api_manager.movies_api.get_movies(params)
        response_data = response.json()

        # Проверка, что кол-во фильмов больше 0
        for item in response_data["movies"]:
            assert (params["minPrice"] < item["price"] < params["maxPrice"]), "Ошибка фильтрации"

    def test_get_movie(self, api_manager: ApiManager):
        """
        Тест на получение информации о фильме
        """
        # Проверка получения фильма с валидным ID
        api_manager.movies_api.get_movie(390)

        # Проверка получения фильма с невалидным ID
        api_manager.movies_api.get_movie(450, expected_status=404)

    def test_create_movie(
            self, api_manager: ApiManager, test_movie,
            test_movie_min_data_item, test_movie_negative_data
    ):
        """
        Тест на создание фильма
        """
        # Авторизация супер юзера
        auth_superuser(api_manager)

        # Проверка создания фильма с валидными данными
        api_manager.movies_api.create_movie(test_movie)

        # Проверка создания фильма с минимальным набором обязательных полей
        api_manager.movies_api.create_movie(test_movie_min_data_item)

        # Проверка создания фильма с отсутствием обязательных полей
        api_manager.movies_api.create_movie(test_movie_negative_data, expected_status=400)

    def test_update_movie(self, api_manager: ApiManager, test_movie):
        """
        Тест на обновление фильма
        """
        # Авторизация супер юзера
        auth_superuser(api_manager)

        # Успешное обновление фильма с валидным ID
        api_manager.movies_api.update_movie(390, test_movie)

        # Изменение фильма с невалидным ID
        api_manager.movies_api.update_movie(450, test_movie, expected_status=404)

    def test_delete_movie(self, api_manager: ApiManager):
        """
        Тест на удаление информации о фильме
        """
        # Авторизация супер юзера
        auth_superuser(api_manager)

        movie_id = 390

        # Успешное удаление фильма с валидным ID
        api_manager.movies_api.delete_movie(movie_id)

        # Проверка, что фильм больше не доступен
        api_manager.movies_api.get_movie(movie_id, expected_status=404)

        # Удаление фильма с невалидным ID
        api_manager.movies_api.delete_movie(movie_id, expected_status=404)
