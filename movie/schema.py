import graphene
from graphene_django import DjangoObjectType

from .models import Movie


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class MovieInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreateMovie(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    movie = graphene.Field(lambda: MovieType)

    @staticmethod
    def mutate(root, info, name):
        movie = Movie(name=name).save()
        ok = True
        return CreateMovie(movie=movie, ok=ok)


class MovieMutations(graphene.ObjectType):
    create_movie = CreateMovie.Field()


class MovieQuery(graphene.ObjectType):
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


schema = graphene.Schema(query=MovieQuery, mutation=MovieMutations)
