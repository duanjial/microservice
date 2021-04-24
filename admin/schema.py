import graphene
from graphene_django import DjangoObjectType

from products.models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("title", "image", "likes")


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product_by_title = graphene.Field(ProductType, title=graphene.String(required=True))

    @staticmethod
    def resolve_all_products(self, root):
        return Product.objects.all()

    @staticmethod
    def resolve_product_by_title(self, root, title):
        try:
            return Product.objects.get(title=title)
        except Product.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
