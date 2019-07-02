import graphene
from graphene_django import DjangoObjectType

from .models import Movie


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class Query(graphene.ObjectType):
    movies = graphene.List(MovieType)

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()


schema = graphene.Schema(query=Query)
