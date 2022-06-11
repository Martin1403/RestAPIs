import click

from sqlalchemy.future import select

from graphqlquartapp.api.models import engine, async_session, Post, User
from graphqlquartapp.api.tests.asyncrun import async_run


@click.command("test-db")
@async_run
async def test_db():
    async with async_session() as session:
        # USER:
        async with session.begin():
            user = User(username="John", email="example@example.xxx", password="12345")
            session.add(user)
        await session.commit()
        click.echo(f"CREATE: {user}\n\n")

        async with session.begin():
            result = await session.execute(select(User).where(User.id == user.id))
            user = result.scalars().first()
        await session.commit()
        click.echo(f"GET: {user}\n\n")

        async with session.begin():
            result = await session.execute(select(User).where(User.id == user.id))
            user = result.scalars().first()
            user.username = "Frederick"
        await session.commit()
        click.echo(f"UPDATE: {user}\n\n")

        async with session.begin():
            result = await session.execute(select(User).order_by(User.id))
            users = result.scalars()
            for user in users:
                await session.delete(user)
                click.echo(f"DELETE: {user}\n\n")
        await session.commit()

        # POST:
        async with session.begin():
            user = User(username="John", email="example@example.xxx", password="12345")
            session.add(user)
        await session.commit()

        async with session.begin():
            post = Post(user_id=user.id, text="Hello World!!!")
            session.add(post)
        await session.commit()
        click.echo(f"CREATE: {user}")
        click.echo(f"CREATE: {post}\n\n")

        async with session.begin():
            result = await session.execute(select(Post).order_by(Post.id))
            posts = result.scalars()
            for post in posts:
                await session.delete(post)
                click.echo(f"DELETE: {post}\n\n")
        await session.commit()

    await engine.dispose()

    click.echo("Database ok...")
