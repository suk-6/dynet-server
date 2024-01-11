from pydantic import BaseModel


class SignupUser(BaseModel):
    email: str
    password: str
    name: str
    studentId: str


class SigninUser(BaseModel):
    email: str
    password: str
