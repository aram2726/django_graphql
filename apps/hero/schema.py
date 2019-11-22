import graphene

from .models import Hero
from .mutators import HeroType, CreateHero, UpdateHero, DeleteHero
from apps.movie.mutators import MovieType


class HeroInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    gender = graphene.String(required=True)
    movie = graphene.Int(required=True)


class HeroMutations(graphene.ObjectType):
    create_hero = CreateHero.Field()
    update_hero = UpdateHero.Field()
    delete_hero = DeleteHero.Field()


class Query(graphene.ObjectType):

    heroes = graphene.List(HeroType)
    hero = graphene.Field(HeroType, id=graphene.Int())

    @staticmethod
    def resolve_heroes(info, **kwargs):
        return Hero.objects.all()

    @staticmethod
    def resolve_movie(info, **kwargs):
        return MovieType()

    @staticmethod
    def resolve_hero(info, **kwargs):
        hero_id = kwargs.get('id')
        if hero_id:
            try:
                return Hero.objects.get(pk=hero_id)
            except Hero.DoesNotExist:
                return None


schema = graphene.Schema(query=Query, mutation=HeroMutations)
