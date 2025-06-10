import allure
from playwright.sync_api import expect
from random import randint

from constants.constants import UI_MOVIES_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT


@allure.epic("Тестирование работы UI")
@allure.feature("Тестирование взаимодействия пользователя с UI регистрации")
class TestRegistrationUser:
    @allure.title("Тест на регистрацию пользователя")
    def test_registration(self, page):

        page.goto(UI_MOVIES_URL + REGISTER_ENDPOINT)

        username_locator = '[data-qa-id="register_full_name_input"]'
        email_locator = '[data-qa-id="register_email_input"]'
        password_locator = '[data-qa-id="register_password_input"]'
        repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

        user_email = f'test{randint(1, 9999)}-admin@email.qa'
        password = "12345qwertY"

        # page.pause()
        page.fill(selector=username_locator, value="Иванов Иван Иванович")
        page.fill(selector=email_locator, value=user_email)
        page.fill(selector=password_locator, value=password)
        page.fill(selector=repeat_password_locator, value=password)

        register_locator = '[data-qa-id="register_submit_button"]'

        page.click(register_locator)

        page.wait_for_url(UI_MOVIES_URL + LOGIN_ENDPOINT)

        expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)
