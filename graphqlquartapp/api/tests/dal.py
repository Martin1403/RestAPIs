import click

from graphqlquartapp.api.dal import user_dal, post_dal
from graphqlquartapp.api.tests.asyncrun import async_run


@click.command("test-dal")
@async_run
async def test_dal():
    async with user_dal() as ud:
        user = await ud.get_user_email(email="example@example.xxx")
    print(user)
    """
    user = dict(username="John", email="example@example.xxx", password="12345")

    async with user_dal() as ud:
        user = await ud.create_user(user)
    click.echo(f"CREATE: {user}\n\n")

    async with user_dal() as ud:
        try:
            user = await ud.get_user_id(id=user.id)
            click.echo(f"GET: {user}\n\n")
        except AttributeError as error:
            click.echo(f"GET: {error}\n\n")

    user = dict(id=user.id, username="David", email="example@example.xxx", password="12345")

    async with user_dal() as ud:
        try:
            user = await ud.update_user(**user)
            click.echo(f"UPDATE: {user}\n\n")
        except AttributeError as error:
            click.echo(f"UPDATE: {error}\n\n")

    post = dict(user_id=user.id, text="Hello World!!!")

    async with post_dal() as pd:
        post = await pd.create_post(**post)
        click.echo(f"CREATE: {post}\n\n")

    async with post_dal() as pd:
        post = await pd.get_post_id(id=post.id)
        click.echo(f"GET: {post}\n\n")

    async with post_dal() as pd:
        posts = await pd.get_posts_user_id(user_id=user.id)
        for post in posts:
            click.echo(f"GET ALL: {post}")
        click.echo("\n\n")

    click.echo(f"POST ID: {post.id}")
    async with post_dal() as pd:
        await pd.delete_post_id(id=post.id)
        click.echo(f"DELETE: {post}")
    
    async with user_dal() as ud:
        try:
            await ud.delete_user_id(id=user.id)
            click.echo(f"DELETE: {user.id}\n\n")
        except AttributeError as error:
            click.echo(f"DELETE: {error}\n\n")
"""
    click.echo(f"Data access layer ok...")
