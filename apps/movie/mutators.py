import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from apps.movie.models import Movie


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class MovieBaseMutator(graphene.Mutation):
    class Arguments:
        movie_id = graphene.Int()
        name = graphene.String()

    @staticmethod
    def mutate(*args, **kwargs):
        raise NotImplemented


class CreateMovie(MovieBaseMutator):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    movie = graphene.Field(lambda: MovieType)

    @staticmethod
    def mutate(root, info, name):
        movie = Movie(name=name).save()
        ok = True
        return CreateMovie(movie=movie, ok=ok)


class UpdateMovie(MovieBaseMutator):
    ok = graphene.Boolean()
    movie = graphene.Field(lambda: MovieType)

    @staticmethod
    def mutate(root, info, movie_id, name):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise GraphQLError("Invalid id %s." % movie_id)

        movie.name = name
        movie.save()
        ok = True
        return UpdateMovie(movie=movie, ok=ok)


class DeleteMovie(MovieBaseMutator):
    ok = graphene.Boolean()
    movie = graphene.Field(lambda: MovieType)

    @staticmethod
    def mutate(root, info, movie_id, name):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise GraphQLError("Invalid id %s." % movie_id)
        movie.delete()
        ok = True
        return DeleteMovie(movie=movie, ok=ok)
