import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from enums.roles import Roles


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
