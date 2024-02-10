from fastapi import Depends
from src.database import get_session
from src.api.user.models import User
from sqlmodel import select, Session


class UserService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get(self):
        statement = select(User)
        users = self.session.exec(statement).all()
        return users

    def create(self, user_create_input):
        user = User(**user_create_input.model_dump())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int):
        statement = select(User).where(User.id == user_id)
        user = self.session.exec(statement).first()
        return user

    def update(self, user_id, user_update_input):
        statement = select(User).where(User.id == user_id)
        user = self.session.exec(statement).one()
        for key, value in user_update_input.dict().items():
            setattr(user, key, value)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id):
        statement = select(User).where(User.id == user_id)
        user = self.session.exec(statement).one()
        self.session.delete(user)
        self.session.commit()
        return user
