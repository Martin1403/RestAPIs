import asyncio
import click
from functools import wraps

from random import choice

from quart_app.api.models import engine, Base
from quart_app.api.dal import user_dal, post_dal
from quart_app.api.utils import AsyncTest, email, text, password


def async_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@click.command("test-async")
@async_run
async def test_async():
    async with AsyncTest() as test:
        async_object = await test
    click.echo(async_object.text)


@click.command("init-db")
@async_run
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    click.echo("Init db ok...")


@click.command("test-dal")
@async_run
async def test_dal():

    user = dict(username=text(20), email=email(), password=password(5))
    async with user_dal() as ud:
        user = await ud.create_user(user)
    click.echo(user)

    async with user_dal() as ud:
        user = user.json()
        user["password"] = password(5)
        user["username"] = text(5)
        user["email"] = email()
        user.pop("date")
        user = await ud.update_user(user)
    click.echo(user)

    async with user_dal() as ud:
        users = await ud.get_users()
    click.echo(users)

    async with user_dal() as ud:
        id = await ud.get_user_id(choice(users).get('id'))
    click.echo(id)

    async with post_dal() as pd:
        post = await pd.create_post_user_id(user_id=choice(users).get('id'), text=text(10))
    click.echo(post)

    async with post_dal() as pd:
        posts = await pd.get_posts_user_id(user_id=choice(users).get('id'))
    click.echo(posts)

    async with post_dal() as pd:
        post = await pd.get_post_id(post.id)
    click.echo(post)

    # async with post_dal() as pd:
    #    await pd.delete_post_id(post.id)

    # async with user_dal() as ud:
    #    await ud.delete_user_id(id=user.id)

    click.echo("Test dal ok...")
