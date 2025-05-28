import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

from enums.roles import Roles

Base = declarative_base()


class UserData(BaseModel):
    email: str
    fullName: str
    password: str = Field(..., min_length=8)
    passwordRepeat: str = Field(..., min_length=1, description="Пароли должны совпадать")
    roles: list[Roles] = [Roles.USER.value]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("email", mode="before")
    def check_email(cls, value: str) -> str:
        """
        Проверка, что поле email содержит в себе символ @
        :param value: email
        """
        if "@" not in value:
            raise ValueError(f"значение {value} должно содержать символ @")
        return value

    @field_validator("passwordRepeat",  mode="before")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value  # Преобразуем Enum в строку
        }


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value


#Модель базы данных для пользователя
class UserDBModel(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(String)


class MovieDBModel(Base):
    """
    Модель для таблицы movies.
    """
    __tablename__ = 'movies'  # Имя таблицы в базе данных

    # Поля таблицы
    id = Column(String, primary_key=True)  # Уникальный идентификатор фильма
    name = Column(String, nullable=False)  # Название фильма
    description = Column(String)  # Описание фильма
    price = Column(Integer, nullable=False)  # Цена фильма
    genre_id = Column(String, ForeignKey('genres.id'), nullable=False)  # Ссылка на жанр
    image_url = Column(String)  # Ссылка на изображение
    location = Column(String)  # Локация фильма (например, "MSK")
    rating = Column(Integer)  # Рейтинг фильма
    published = Column(Boolean)  # Опубликован ли фильм
    created_at = Column(DateTime)  # Дата создания записи