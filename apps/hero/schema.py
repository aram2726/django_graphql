import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Hero
from apps.movie.schema import MovieType


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero


class HeroInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    gender = graphene.String(required=True)
    movie = graphene.Int(required=True)


class CreateHero(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        gender = graphene.String()
        movie = graphene.Int()

    ok = graphene.Boolean()
    hero = graphene.Field(lambda: HeroType)

    @staticmethod
    def mutate(root, info, name, gender, movie):
        hero = Hero(name=name, gender=gender, movie_id=movie).save()
        ok = True
        return CreateHero(hero=hero, ok=ok)


class UpdateHero(graphene.Mutation):
    class Arguments:
        hero_id = graphene.Int()
        name = graphene.String()
        gender = graphene.String()
        movie_id = graphene.Int()

    ok = graphene.Boolean()
    hero = graphene.Field(lambda: HeroType)

    @staticmethod
    def mutate(root, info, hero_id, **kwargs):
        try:
            hero = Hero.objects.get(pk=hero_id)
        except Hero.DoesNotExist:
            raise GraphQLError("Invalid id %s." % hero_id)

        for item in kwargs:
            setattr(hero, item, kwargs[item])
        hero.save()

        ok = True
        return UpdateHero(hero=hero, ok=ok)


class HeroMutations(graphene.ObjectType):
    create_hero = CreateHero.Field()
    update_hero = UpdateHero.Field()


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


schema = graphene.Schema(query=Query, mutation=HeroMutations)
