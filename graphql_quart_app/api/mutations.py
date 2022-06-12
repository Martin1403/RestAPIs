from ariadne import MutationType

from graphqlquartapp.api.dal import user_dal, post_dal

mutation = MutationType()


@mutation.field("CreateUser")
async def create_user_resolver(*_, input):
    async with user_dal() as ud:
        user = await ud.create_user(input)
    return user.json() if user else None


@mutation.field("CreatePost")
async def create_post_resolver(*_, input):
    async with post_dal() as pd:
        post = await pd.create_post(**input)
    return post.json() if post else None


@mutation.field("UpdateUser")
async def update_user_resolver(*_, input):
    async with user_dal() as ud:
        user = await ud.update_user(input)
    return user.json() if user else None
