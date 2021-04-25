from graphene_django import DjangoObjectType
from products.models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"
