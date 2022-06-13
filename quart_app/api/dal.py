from random import choice
from contextlib import asynccontextmanager

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError, InvalidRequestError
from sqlalchemy.orm.exc import StaleDataError
from werkzeug.security import generate_password_hash

from quart_app.api.models import async_session, User, Post, engine


class UserDAL(object):
    """Data access layer"""

    def __init__(self, session):
        self.db_session = session

    async def create_user(self, data):
        try:
            user = User(**data)
            self.db_session.add(user)
            await self.db_session.flush()
            return user
        except (IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            return None

    async def get_users(self):
        result = await self.db_session.execute(select(User).order_by(User.id))
        return [user.json() for user in result.scalars().all()]

    async def get_user_id(self, id):
        try:
            result = await self.db_session.execute(select(User).where(User.id == id))
            user = result.scalars().first()
            if isinstance(user, User):
                return user
            else:
                return None
        except (IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            return None

    async def update_user(self, data):
        try:
            user = await self.get_user_id(data.get("id"))
            if isinstance(user, User):
                user.username = data.get("username") or user.username
                user.password_hash = generate_password_hash(data.get("password")) or user.password_hash
                user.email = data.get("email") or user.email
                user.picture = data.get("picture") or user.picture
                await self.db_session.commit()
                return user
            else:
                return None
        except (IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            return None

    async def delete_user_id(self, id):
        user = await self.get_user_id(id=id)
        try:
            if isinstance(user, User):
                await self.db_session.delete(user)
                await self.db_session.flush()
        except (IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            pass


class PostDAL(object):
    """Post Data Access Layer"""
    def __init__(self, session):
        self.db_session = session

    async def get_posts(self):
        result = await self.db_session.execute(select(Post).order_by(Post.id))
        return [post.json() for post in result.scalars().all()]

    async def get_posts_user_id(self, user_id):
        result = await self.db_session.execute(select(Post).where(Post.userId == user_id))
        return [post.json() for post in result.scalars().all()]

    async def create_post_user_id(self, user_id, text):
        post = Post(user_id=user_id, text=text)
        try:
            if isinstance(post, Post):
                self.db_session.add(post)
                await self.db_session.commit()
                return post
            else:
                return None
        except (IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            return post

    async def get_post_id(self, id):
        try:
            result = await self.db_session.execute(select(Post).where(Post.id == id))
            post = result.scalars().first()
            return post if isinstance(post, Post) else None
        except (IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            return None

    async def delete_post_id(self, id):
        try:
            post = await self.get_post_id(id=id)
            if isinstance(post, Post):
                await self.db_session.delete(post)
                await self.db_session.flush()
        except (IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            pass


@asynccontextmanager
async def user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)


@asynccontextmanager
async def post_dal():
    async with async_session() as session:
        async with session.begin():
            yield PostDAL(session)
