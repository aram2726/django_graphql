import graphene
from graphene_django import DjangoObjectType

from .models import Movie


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        # only_fields
        # exclude_fields

    # extra_field = graphne.<SomeField>
    # def resolve_extra_field(self, info)

    # @classmethod
    # def get_queryset(cls, queryset, info): ...


class Query(graphene.ObjectType):
    movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int())

    def resolve_movies(self, info, **kwargs):
        # if info.context.user.is_authenticated():
        return Movie.objects.all()

    def resolve_movie(self, info, **kwargs):
        movie_id = kwargs.get("id")
        try:
            return Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
