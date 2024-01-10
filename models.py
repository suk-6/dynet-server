from pydantic import BaseModel


class SignupUser(BaseModel):
    email: str
    password: str
    name: str


class SigninUser(BaseModel):
    email: str
    password: str
