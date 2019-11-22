import graphene

from apps.movie.mutators import MovieType, CreateMovie, UpdateMovie, DeleteMovie
from .models import Movie


class MovieInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class MovieMutations(graphene.ObjectType):
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()


class MovieQuery(graphene.ObjectType):
    movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int())

    @staticmethod
    def resolve_movies(info, **kwargs):
        return Movie.objects.all()

    @staticmethod
    def resolve_movie(info, **kwargs):
        movie_id = kwargs.get("id")
        try:
            return Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return None


schema = graphene.Schema(query=MovieQuery, mutation=MovieMutations)

