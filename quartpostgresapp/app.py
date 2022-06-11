import asyncio
from typing import Tuple, Optional, List
from dataclasses import asdict

from pydantic.dataclasses import dataclass
from databases import Database
from quart import Quart, redirect
from quart_schema import QuartSchema, hide_route
from quart_schema import validate_request, validate_response, validate_querystring

app = Quart(__name__)
app.config["DATABASE_URL"] = "postgresql://postgres:password@localhost:5432/postgres"

QuartSchema(app)


@app.route("/")
@hide_route
def index():
    return redirect("/docs")


"""
@app.route("/")
async def index() -> str:
    count_todos = await app.db.fetch_val("SELECT COUNT(*) FROM todos")
    return f"There are {count_todos} todos"
"""


@dataclass
class TodoData:
    complete: bool
    size: str
    task: str


@dataclass
class Todo(TodoData):
    id: int


@app.route("/todos/", methods=["POST"])
@validate_request(TodoData)
@validate_response(Todo, status_code=201)
async def create_todo(data: TodoData) -> Tuple[Todo, int]:
    """Create a new Todo
    This allows todos to be created and stored.
    """
    id_ = await app.db.fetch_val(
        """INSERT INTO todos (complete, size, task)
                VALUES (:complete, :size, :task)
             RETURNING id""",
        values=asdict(data)
    )
    return Todo(id=id_, **asdict(data)), 201


@dataclass
class Todos:
    todos: List[Todo]


@dataclass
class TodoFilter:
    complete: Optional[bool] = None


@app.route("/todos/", methods=["GET"])
@validate_response(Todos)
@validate_querystring(TodoFilter)
async def get_todos(query_args: TodoFilter) -> Todos:
    """Return all Todos
    This return all todos in database.
    """
    if query_args.complete is None:
        result = await app.db.fetch_all(
            """SELECT id, complete, size, task
                 FROM todos"""
        )
    else:
        result = await app.db.fetch_all(
            """SELECT id, complete, size, task
                 FROM todos
                WHERE complete = :complete""",
            values=asdict(query_args),
        )
    todos = [Todo(**row) for row in result]
    return Todos(todos=todos)


@app.route("/todos/<int:id>/", methods=["PUT"])
@validate_request(TodoData)
@validate_response(Todo)
async def update_todo(id: int, data: TodoData) -> Todo:
    """Update the todo
    This allows the todo to be replace with the request data.
    """
    todo = Todo(id=id, **asdict(data))
    await app.db.execute(
        """UPDATE todos
              SET complete = :complete, size = :size, task = :task 
            WHERE id = :id""",
        values=asdict(todo)
    )
    return todo


@app.route("/todos/<int:id>/", methods=["DELETE"])
async def delete_todo(id: int) -> Tuple[str, int]:
    """Delete todo.
    Delete todo from database.
    """
    await app.db.execute(
        """DELETE FROM todos WHERE id = :id""",
        values={"id": id}
    )
    return "", 202


async def _create_db_connection() -> Database:
    db = Database(app.config["DATABASE_URL"])
    await db.connect()
    return db


@app.before_serving
async def startup() -> None:
    app.db = await _create_db_connection()


@app.cli.command("init-db")
def init_db() -> None:
    async def _inner() -> None:
        db = await _create_db_connection()
        with open("quartpostgresapp/schema.sql", "r") as file_:
            print("Table created.")
            for command in file_.read().split(";"):
                await db.execute(command)
    asyncio.run(_inner())
