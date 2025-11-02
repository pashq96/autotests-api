from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, field_validator

from tools.fakers import get_random_email


class UserSchema(BaseModel):
    """
    Описание структуры пользователя.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

    # Проверка на то что str поле id подходит под структуру UUID
    @field_validator('id')
    def validate_uuid(cls, v):
        try:
            UUID(v)
        except ValueError:
            raise ValueError(f"{v} is not a valid UUID string")
        return v


class CreateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание юзера.
    """
    email: EmailStr = Field(default_factory=get_random_email)
    password: str = Field(default="password")
    last_name: str = Field(alias="lastName", default="default_last_name")
    first_name: str = Field(alias="firstName", default="default_first_name")
    middle_name: str = Field(alias="middleName", default="default_middle_name")


class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа создания пользователя.
    """
    user: UserSchema
