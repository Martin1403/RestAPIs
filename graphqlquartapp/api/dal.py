from contextlib import asynccontextmanager

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from graphqlquartapp.api.models import async_session, User, Post, engine


class SomeException(Exception):
    pass


class UserDAL(object):
    """User Data Access Layer"""
    def __init__(self, session):
        self.db_session = session

    async def create_user(self, input):
        user = User(**input)
        try:
            self.db_session.add(user)
            await self.db_session.commit()
            return user
        except IntegrityError:
            return

    async def get_user_email(self, email):
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_user_id(self, id):
        result = await self.db_session.execute(select(User).where(User.id == id))
        return result.scalars().first()

    async def update_user(self, kwargs):
        try:
            user = await self.get_user_id(kwargs.get('id'))
            user.username = kwargs.get('new_username') or user.username
            user.password_hash = generate_password_hash(kwargs.get("password")) or user.password_hash
            user.email = kwargs.get("email") or user.email
            user.picture = kwargs.get("picture") or user.picture
            await self.db_session.flush()
            return user
        except SomeException:
            return

    async def delete_user_id(self, id):
        user = await self.get_user_id(id=id)
        await self.db_session.delete(user)


class PostDAL(object):
    """Post Data Access Layer"""
    def __init__(self, session):
        self.db_session = session

    async def get_posts_by_user_id(self, user_id):
        result = await self.db_session.execute(select(Post).where(Post.userId == user_id))
        return [post for post in result.scalars().all()]

    async def create_post(self, user_id, user_text, ai_text, user_date, ai_date):
        post = Post(user_id=user_id, user_text=user_text, ai_text=ai_text, user_date=user_date, ai_date=ai_date)
        self.db_session.add(post)
        await self.db_session.commit()
        return post

    async def get_post_id(self, id):
        result = await self.db_session.execute(select(Post).where(Post.id == id))
        return result.scalars().first()

    async def delete_post_id(self, id):
        post = await self.get_post_id(id=id)
        await self.db_session.delete(post)
        await self.db_session.commit()


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
