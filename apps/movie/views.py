from graphene_django.views import GraphQLView

from .schema import schema as movie_schema


class MovieView(GraphQLView):
    graphiql = True
    schema = movie_schema
