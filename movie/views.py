from graphene_django.views import GraphQLView

from .schema import schema

movie_view = GraphQLView.as_view(graphiql=True, schema=schema)