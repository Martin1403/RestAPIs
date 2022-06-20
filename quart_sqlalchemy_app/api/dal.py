from contextlib import asynccontextmanager

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError, InvalidRequestError, TimeoutError
from sqlalchemy.orm.exc import StaleDataError
from werkzeug.security import generate_password_hash

from quart_sqlalchemy_app.api.models import async_session, User, Post


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
        except (TimeoutError, IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            return None

    async def get_users(self):
        try:
            result = await self.db_session.execute(select(User).order_by(User.id))
            if result:
                return [user.json() for user in result.scalars().all()]
        except TimeoutError:
            pass
        return []

    async def get_user_id(self, id):
        if id:
            try:
                result = await self.db_session.execute(select(User).where(User.id == id))
                if result:
                    return result.scalars().first()
            except TimeoutError:
                pass
        return None

    async def update_user(self, data):
        try:
            user = await self.get_user_id(data.get("id"))
            if user:
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
            if user:
                await self.db_session.delete(user)
                await self.db_session.flush()
        except (IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            pass


class PostDAL(object):
    """Post Data Access Layer"""
    def __init__(self, session):
        self.db_session = session

    async def get_posts(self):
        try:
            result = await self.db_session.execute(select(Post).order_by(Post.id))
            if result:
                return [post.json() for post in result.scalars().all()]
        except TimeoutError:
            pass
        return []

    async def get_posts_user_id(self, user_id):
        if user_id:
            try:
                result = await self.db_session.execute(select(Post).where(Post.userId == user_id))
                if result:
                    return [post.json() for post in result.scalars().all()]
            except TimeoutError:
                pass
        return []

    async def create_post_user_id(self, user_id, text):

        if user_id:
            try:
                post = Post(user_id=user_id, text=text)
                self.db_session.add(post)
                await self.db_session.commit()
                return post
            except (TimeoutError, IntegrityError, OperationalError):
                pass
        return None

    async def get_post_id(self, id):
        try:
            result = await self.db_session.execute(select(Post).where(Post.id == id))
            post = result.scalars().first()
            return post
        except (TimeoutError, IntegrityError, OperationalError, InvalidRequestError, StaleDataError):
            return None

    async def delete_post_id(self, id):
        try:
            post = await self.get_post_id(id=id)
            if post:
                await self.db_session.delete(post)
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
