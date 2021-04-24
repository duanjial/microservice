import graphene
from graphene_django import DjangoObjectType

from products.models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "title", "image", "likes")


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(self, root):
        return Product.objects.all()


schema = graphene.Schema(query=Query)
