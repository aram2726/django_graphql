import graphene
from graphene_django import DjangoObjectType

from .models import Hero
from movie.schema import MovieType


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero


class Query(graphene.ObjectType):
    heroes = graphene.List(HeroType)
    hero = graphene.Field(HeroType, id=graphene.Int())

    def resolve_heroes(self, info, **kwargs):
        return Hero.objects.all()

    def resolve_movie(self, info, **kwargs):
        return MovieType()

    def resolve_hero(self, info, **kwargs):
        hero_id = kwargs.get('id')
        if hero_id:
            try:
                return Hero.objects.get(pk=hero_id)
            except Hero.DoesNotExist:
                return None


schema = graphene.Schema(query=Query)
