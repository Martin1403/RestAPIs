import string
from random import choice


def text(x):
    return "".join([choice(string.ascii_lowercase) for _ in range(x)])


def password(x):
    return "".join([choice(string.digits) for _ in range(x)])


def email():
    return f"{text(10)}@{text(10)}.{text(3)}"


class AsyncTest(object):
    """Async Class"""
    def __init__(self):
        self.text = "HelloWorld!!!"

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def __await__(self):
        return self.__aenter__().__await__()

