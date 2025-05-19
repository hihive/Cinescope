import random
import string

from faker import Faker

faker = Faker('ru_RU')


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = "".join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_random_movie():
        """
        Генерация случайного фильма для тестов.
        """
        return {
            "name": faker.catch_phrase(),
            "price": random.randint(100, 1000),
            "description": faker.text(max_nb_chars=200),
            "location": random.choice(["MSK", "SPB"]),
            "published": True,
            "rating": random.randint(1, 10),
            "genreId": 3,
        }
