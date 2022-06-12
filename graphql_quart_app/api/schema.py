from pathlib import Path

from ariadne import make_executable_schema

from graphqlquartapp.api.queries import query
from graphqlquartapp.api.mutations import mutation

schema = make_executable_schema(
    (Path(__file__).parent / 'schema.graphql').read_text(),
    [query, mutation, ]
)
