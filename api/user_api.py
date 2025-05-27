from custom_requester.custom_requester import CustomRequester
from constants.constants import USER_URL


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        self.session = session
        super().__init__(session=session, base_url=USER_URL)

    def get_user(self, user_locator, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_locator: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """

        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_locator}",
            expected_status=expected_status,
        )

    def create_user(self, user_data, expected_status=201):
        """
        Создание пользователя
        :param user_data: данные для создания пользователя.
        :param expected_status: Ожидаемый статус-код.
        """

        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """

        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )
