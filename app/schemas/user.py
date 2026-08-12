from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=72
    )

    role: str = "Customer"


class UserLogin(BaseModel):
    username: str
    password: str