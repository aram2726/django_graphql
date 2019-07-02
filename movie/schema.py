import graphene
from graphene_django import DjangoObjectType

from .models import Movie


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class Query(graphene.ObjectType):
    movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int())

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()

    def resolve_movie(self, info, **kwargs):
        movie_id = kwargs.get("id")
        try:
            return Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
