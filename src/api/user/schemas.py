from pydantic import BaseModel


class UserCreateInput(BaseModel):
    name: str
    email: str
    password: str


class UserUpdateInput(UserCreateInput):
    pass
