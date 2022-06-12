import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

# MAKE DATABASE DIRECTORY
base = os.path.abspath(os.path.dirname(__name__))
database = os.path.join(base, "flaskapp/database")
os.makedirs(database, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{database}/test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"Username {self.username}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password_hash,
        }
