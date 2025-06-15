import allure
import pytest

from models.page_object_models import CinescopLoginPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestLoginUser:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, page, common_user):
        login_page = CinescopLoginPage(page)

        login_page.open()
        # page.pause()
        login_page.login(common_user.email, common_user.password)

        login_page.assert_was_redirect_to_home_page()
        login_page.make_screenshot_and_attach_to_allure()
        login_page.assert_alert_was_pop_us()
