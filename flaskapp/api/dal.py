from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError
from flask import abort
from werkzeug.security import generate_password_hash

from flaskapp.api.models import SessionLocal, User


class UserDAL(object):
    """User DataAccessLayer"""

    def __init__(self, session):
        self.db_session = session

    def register_user(self, data):
        new_user = User(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )
        try:
            self.db_session.add(new_user)
            self.db_session.commit()
            self.db_session.refresh(new_user)
            return new_user.json()
        except IntegrityError as error:
            abort(500, description=f'Some credentials are already used.')

    def get_user_id(self, user_id):
        return self.db_session.query(User).filter(User.user_id == user_id).first()

    def get_all_users(self):
        users = self.db_session.query(User).all()
        return {"users": [user.json() for user in users]}

    def update_user_id(self, user_id, data):
        user = self.get_user_id(user_id)
        if user:
            user.username = data.get("username")
            user.email = data.get("email")
            user.password_hash = generate_password_hash(
                data.get("password"))
            self.db_session.commit()
            self.db_session.refresh(user)
            return user.json()
        return

    def delete_user_id(self, user_id):
        user = self.get_user_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            return user
        return


@contextmanager
def user_dal():
    with SessionLocal() as session:
        yield UserDAL(session)
