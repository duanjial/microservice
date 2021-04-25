import graphene
from my_graphql.ProductType import ProductType
from products.models import Product
from products.serializers import ProductSerializer
from graphene.types.scalars import Scalar


class ObjectField(Scalar):
    @staticmethod
    def serialize(dt):
        return dt


class UpdateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        image = graphene.String()
        product_id = graphene.ID(required=True)
    product = graphene.Field(ProductType)
    message = ObjectField()
    status = graphene.Int()

    @classmethod
    def mutate(cls, root, info, product_id, **kwargs):
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(instance=product, data=kwargs, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg = "success"
        else:
            product = None
            msg = serializer.errors
        return cls(product=product, message=msg, status=204)


class CreateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        image = graphene.String()
    product = graphene.Field(ProductType)
    message = ObjectField()
    status = graphene.Int()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        serializer = ProductSerializer(data=kwargs)
        if serializer.is_valid():
            product = serializer.save()
            msg = "success"
        else:
            msg = serializer.errors
            product = None
        return cls(product=product, message=msg, status=201)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)
    message = ObjectField()
    status = graphene.Int()

    @classmethod
    def mutate(cls, root, info, product_id, **kwargs):
        product = Product.objects.get(id=product_id)
        product.delete()
        return cls(message="deleted", status=204)
