import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Hero


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero


class HeroBaseMutation(graphene.Mutation):
    class Arguments:
        hero_id = graphene.Int()
        name = graphene.String()
        gender = graphene.String()
        movie = graphene.Int()

    @staticmethod
    def mutate(*args, **kwargs):
        raise NotImplemented


class CreateHero(HeroBaseMutation):

    ok = graphene.Boolean()
    hero = graphene.Field(lambda: HeroType)

    @staticmethod
    def mutate(root, info, name, gender, movie):
        hero = Hero(name=name, gender=gender, movie_id=movie).save()
        ok = True
        return CreateHero(hero=hero, ok=ok)


class UpdateHero(HeroBaseMutation):

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


class DeleteHero(HeroBaseMutation):

    ok = graphene.Boolean()
    hero = graphene.Field(lambda: HeroType)

    @staticmethod
    def mutate(root, info, hero_id, **kwargs):
        try:
            hero = Hero.objects.get(pk=hero_id)
        except Hero.DoesNotExist:
            raise GraphQLError("Invalid id %s." % hero_id)
        hero.delete()
        ok = True
        return DeleteHero(hero=hero, ok=ok)
