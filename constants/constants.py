import os

from dotenv import load_dotenv

USER_URL = "https://auth.dev-cinescope.coconutqa.ru"
MOVIES_URL = "https://api.dev-cinescope.coconutqa.ru"
UI_MOVIES_URL = "https://dev-cinescope.coconutqa.ru"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"


INVALID_MOVIE_ID = 99999

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'


load_dotenv()
DB_USERNAME = os.getenv("USERNAME")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_PORT = os.getenv("PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")