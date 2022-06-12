import click
import asyncio
from functools import wraps

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update


class Test(object):

    async def __aenter__(self):
        print("enter")

    async def __aexit__(self, *args):
        print("exit")

    def __await__(self):
        return self.__aenter__().__await__()


def async_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@click.command("test-async")
@async_run
async def test_async():
    async with Test():
        print("Hello")
    await Test()
    click.echo("Async ok...")
