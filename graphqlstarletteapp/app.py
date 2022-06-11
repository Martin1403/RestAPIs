import json

from ariadne import MutationType, SubscriptionType, make_executable_schema
from ariadne.asgi import GraphQL
from broadcaster import Broadcast
from starlette.applications import Starlette


broadcast = Broadcast("memory://")


type_defs = """
  type Query {
    _unused: Boolean
  }

  type Message {
    sender: String
    message: String
  }

  type Mutation {
    send(sender: String!, message: String!): Boolean
  }

  type Subscription {
    message: Message
  }
"""


mutation = MutationType()


@mutation.field("send")
async def resolve_send(*_, **message):
    await broadcast.publish(channel="chatroom", message=json.dumps(message))
    return True


subscription = SubscriptionType()


@subscription.source("message")
async def source_message(_, info):
    async with broadcast.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            yield json.loads(event.message)


schema = make_executable_schema(type_defs, mutation, subscription)
graphql = GraphQL(schema=schema, debug=True)

app = Starlette(
    debug=True,
    on_startup=[broadcast.connect],
    on_shutdown=[broadcast.disconnect],
)

app.mount("/", graphql)
