import uuid
import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, String, ForeignKey, Text, Date
from werkzeug.security import generate_password_hash, check_password_hash

from graphqlquartapp.app import app


# SA Engine init
DATABASE_URL = f"sqlite+aiosqlite:///{app.config['DATABASE_URI_PATH']}"
engine = create_async_engine(DATABASE_URL, future=True, echo=app.debug)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


def generate_uuid():
    return uuid.uuid4()


def generate_timestamp():
    return datetime.datetime.now()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    posts = relationship("Post", uselist=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String, unique=False, nullable=False)
    picture = Column(String, nullable=False, default="user.png")
    date = Column(Date, nullable=False, default=generate_timestamp)
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent-to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    def __init__(self, username: str, email: str, password: str) -> None:
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self) -> str:
        return f"<User: {self.username} ID: {self.id}>"

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
    user_text = Column(Text, nullable=False)
    ai_text = Column(Text, nullable=False)
    user_date = Column(String, nullable=False)
    ai_date = Column(String, nullable=False)

    def __init__(self, user_id, user_text, ai_text, user_date, ai_date) -> None:
        self.userId = user_id
        self.ai_text = ai_text
        self.user_text = user_text
        self.ai_date = ai_date
        self.user_date = user_date

    def __repr__(self) -> str:
        return f"<Post: {self.userId} >"

    def json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.userId,
            "ai_text": self.ai_text,
            "user_text": self.user_text,
            "user_date": self.user_date,
            "ai_date": self.ai_date
        }
