from graphene_django.views import GraphQLView

from .schema import schema as hero_schema


class HeroView(GraphQLView):
    graphiql = True
    schema = hero_schema
