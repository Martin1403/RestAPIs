from ariadne import QueryType

from graphqlquartapp.api.dal import user_dal, post_dal

query = QueryType()


@query.field("greeting")
def resolve_greeting(*_):
    return "Hello World!"


@query.field("login")
async def get_user_by_email_resolver(*_, email, password):
    async with user_dal() as ud:
        user = await ud.get_user_email(email=email)
        if user:
            return user if user.check_password(password) else None
    return None


@query.field("delete")
async def delete_user_by_id_resolver(*_, id):
    async with user_dal() as ud:
        user = await ud.delete_user_id(id=id)
    return user


@query.field("user")
async def get_user_by_username_resolver(*_, username):
    async with user_dal() as ud:
        user = await ud.get_user_by_username(username=username)
    return user


@query.field("posts")
async def get_posts_by_user_id_resolver(*_, user_id):
    async with post_dal() as pd:
        posts = await pd.get_posts_by_user_id(user_id=user_id)
    return posts
