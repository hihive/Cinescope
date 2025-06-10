import allure
from playwright.sync_api import expect

from constants.constants import UI_MOVIES_URL, LOGIN_ENDPOINT


@allure.epic("Тестирование работы UI")
@allure.feature("Тестирование взаимодействия авторизованного пользователя с UI")
class TestLoginUser:
    @allure.title("Тест на авторизацию существующего пользователя")
    def test_login(self, page, common_user):

        page.goto(UI_MOVIES_URL + LOGIN_ENDPOINT)

        email_locator = "[data-qa-id='login_email_input']"
        password_locator = "[data-qa-id='login_password_input']"

        # page.pause()
        page.fill(selector=email_locator, value=common_user.email)
        page.fill(selector=password_locator, value=common_user.password)

        login_locator = "[data-qa-id='login_submit_button']"

        page.click(login_locator)

        page.wait_for_url(UI_MOVIES_URL)
        expect(page.get_by_text("Вы вошли в аккаунт")).to_be_visible(visible=True)
