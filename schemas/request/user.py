from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str


class UserRegisterIn(BaseUser):
    password: str
    phone: str
    first_name: str
    last_name: str
    iban: str


class UserLogin(BaseUser):
    password: str
