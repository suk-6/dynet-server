from pydantic import BaseModel


class SigninUser(BaseModel):
    id: str
    password: str


class PasswordChange(BaseModel):
    id: str
    password: str
    newPassword: str
