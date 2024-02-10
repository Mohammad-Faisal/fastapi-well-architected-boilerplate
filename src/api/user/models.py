from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
