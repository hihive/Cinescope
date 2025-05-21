from constants.constants import MOVIES_URL
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    """
    Класс для работы с API фильмов.
    """

    def __init__(self, session):
        self.session = session
        super().__init__(session=session, base_url=MOVIES_URL)

    def get_movies(self, params=None, expected_status=200):
        """
        Получение информации о фильмах
        :param params: Query-параметры.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint="/movies",
            params=params,
            expected_status=expected_status,
        )

    def get_movie(self, movie_id, expected_status=200):
        """
        Получение информации о фильме
        :param movie_id: ID фильма
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, movies_data, expected_status=201):
        """
        Создание фильма
        :param movies_data: Данные для создания фильма
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=f"/movies",
            data=movies_data,
            expected_status=expected_status,
        )

    def update_movie(self, movie_id, movies_data, expected_status=200):
        """
        Изменение существующего фильма
        :param movie_id:
        :param movies_data:
        :param expected_status:
        :return:
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{movie_id}",
            data=movies_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        Удаление фильма
        :param movie_id: ID фильма
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )
