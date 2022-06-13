import os
import uuid
from datetime import datetime

import shortuuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, String, ForeignKey, Text, Date
from werkzeug.security import generate_password_hash, check_password_hash


# SA Engine init
DATABASE_FOLDER = f"{os.path.abspath(os.path.dirname(__name__))}{os.sep}quart_app{os.sep}database"
os.makedirs(DATABASE_FOLDER, exist_ok=True)
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FOLDER}/test.db"
engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


def generate_uuid():
    return shortuuid.encode(uuid.uuid4())


def generate_time():
    return datetime.now()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    posts = relationship("Post", uselist=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String, unique=False, nullable=False)
    picture = Column(String, nullable=False, default="user.png")
    date = Column(String, nullable=False, default=generate_time)

    __mapper_args__ = {
        "eager_defaults": True,
        "confirm_deleted_rows": False,
    }

    def __init__(self, username: str, email: str, password: str, picture="user.png") -> None:
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.picture = picture

    def __repr__(self) -> str:
        return f"<User: {self.username} ID: {self.id} >"

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def json(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "date": self.date,
            "picture": self.picture
        }


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=generate_uuid)
    userId = Column(String, ForeignKey("users.id"))
    text = Column(Text, nullable=False)
    date = Column(String, nullable=False, default=generate_time)

    __mapper_args__ = {
        "eager_defaults": True,
        "confirm_deleted_rows": False,
    }

    def __init__(self, user_id, text) -> None:
        self.userId = user_id
        self.text = text

    def __repr__(self) -> str:
        return f"<Post: {self.userId} >"

    def json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.userId,
            "text": self.text,
            "date": self.date
        }
