import allure
import pytest

from models.page_object_models import CinescopRegisterPage
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegistrationUser:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, page):
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        register_page = CinescopRegisterPage(page)

        register_page.open()
        # page.pause()
        register_page.register(
            full_name=f"PlaywrightTest {random_name}",
            email=random_email,
            password=random_password,
            confirm_password=random_password
        )

        register_page.assert_was_redirect_to_login_page()
        register_page.make_screenshot_and_attach_to_allure()
        register_page.assert_alert_was_pop_up()
