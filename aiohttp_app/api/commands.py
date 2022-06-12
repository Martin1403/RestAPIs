import string
from random import choice
import asyncio
import click
from functools import wraps

from api.models import engine, Base
from api.dal import user_dal, post_dal


def text(x):
    return "".join([choice(string.ascii_lowercase) for _ in range(x)])


def password(x):
    return "".join([choice(string.digits) for _ in range(x)])


def email():
    return f"{text(10)}@{text(10)}.{text(3)}"


def async_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@click.command()
@click.option("--mode", default="init", help="Initialize database.")
@async_run
async def command(mode):
    if mode == "init":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()
        click.echo("Initialize ok...")
    elif mode == "dal":
        user = dict(username=text(20), email=email(), password=password(5))
        async with user_dal() as ud:
            user = await ud.create_user(user)

        async with user_dal() as ud:
            async with user_dal() as uud:
                users = await uud.get_users()
            user = await ud.get_user_id(choice(users).id)

        user = choice(users).json()
        user["password"] = "123456"
        user["username"] = "Alice"
        user["email"] = "xxx@xxx.xxx"
        user.pop("date")

        async with user_dal() as ud:
            user = await ud.update_user(user)

        async with post_dal() as pd:
            post = await pd.create_post_user_id(user_id=choice(users).id, text=text(10))

        user = dict(username=text(20), email=email(), password=password(5))
        async with user_dal() as ud:
            user = await ud.create_user(user)

        async with post_dal() as pd:
            posts = await pd.get_posts_user_id(user_id=choice(users).id)

        async with post_dal() as pd:
            post = await pd.get_post_id(post.id)

        user = dict(username=text(20), email=email(), password=password(5))
        async with user_dal() as ud:
            user = await ud.create_user(user)

        async with post_dal() as pd:
            post = await pd.delete_post_id(post.id)

        async with user_dal() as ud:
            await ud.delete_user_id(id=choice(users).id)

        async with post_dal() as pd:
            posts = await pd.get_posts()
            await pd.delete_post_id(choice(posts).id)
        click.echo(posts)
