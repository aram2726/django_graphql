import graphene
from graphene_django import DjangoObjectType

from .models import Hero
from movie.schema import MovieType


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero


class Query(graphene.ObjectType):
    heroes = graphene.List(HeroType)
    def resolve_heroes(self, info, **kwargs):
        return Hero.objects.all()

    def resolve_movie(self, info, **kwargs):
        return MovieType()

schema = graphene.Schema(query=Query)
