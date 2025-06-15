import typing

import allure
from playwright.async_api import Page

from constants.constants import REGISTER_ENDPOINT, UI_MOVIES_URL, ALL_MOVIES_ENDPOINT, LOGIN_ENDPOINT, UI_HOME_PAGE_URL


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str):
        self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        self.page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url)
        assert self.page.url == url, f"Редирект на {url} не произошел"

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str):
        return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self,locator: str, state: typing.Optional[
                             typing.Literal["attached", "detached", "hidden", "visible"]
                         ] = "visible"):
        self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страиницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)

        with open(screenshot_path, "rb") as file:
            allure.attach(
                file.read(),
                name="Screenshot after redirect",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str):

        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            notification_locator.wait_for(state="hidden")
            assert notification_locator.is_visible() == False, "Уведомление не исчезло"


class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = UI_HOME_PAGE_URL

        self.home_button = "a[href='/' and text()='Cinescope']"
        self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

    def go_to_home_page(self):
        """Переход на главную страницу."""
        self.page.click(self.home_button)
        self.page.wait_for_url(self.home_url)

    def go_to_all_movies(self):
        """Переход на страницу 'Все фильмы'."""
        self.page.click(self.all_movies_button)
        self.page.wait_for_url(f"{self.home_url}{ALL_MOVIES_ENDPOINT}")


class CinescopRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}{REGISTER_ENDPOINT}"

        self.full_name_input = "input[name='fullName']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.confirm_password_input = "input[name='passwordRepeat']"
        self.register_button = "button[data-qa-id='register_submit_button']"

    # Тело страницы
    def open(self):
        """Переход на страницу регистрации."""
        self.page.goto(self.url)

    # Вспомогательные action методы
    def register(self, full_name: str, email: str, password: str, confirm_password: str):
        """Полный процесс регистрации."""
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.confirm_password_input, confirm_password)
        self.click_element(self.register_button)

    def assert_was_redirect_to_login_page(self):
        self.wait_redirect_for_url(f"{self.home_url}login")

    def assert_alert_was_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")


class CinescopLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}{LOGIN_ENDPOINT}"

        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.login_button = "button[data-qa-id='login_submit_button']"

    # Тело страницы
    def open(self):
        """Переход на страницу входа"""
        self.page.goto(self.url)

    def login(self, email: str, password: str):
        """Полный процесс входа"""
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.click_element(self.login_button)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_alert_was_pop_us(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")