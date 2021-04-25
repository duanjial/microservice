from graphene_django import DjangoObjectType
from products.models import Product
from graphene import relay, Int


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"
        interfaces = (relay.Node,)


class ProductConnection(relay.Connection):
    class Meta:
        node = ProductType

