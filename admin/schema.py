import graphene
from graphene_django import DjangoObjectType

from products.models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("title", "image", "likes")


class UpdateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        image = graphene.String()
        product_id = graphene.ID(required=True)
    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, product_id, title, image):
        product = Product.objects.get(id=product_id)
        product.title = title
        product.image = image
        product.save()
        return UpdateProduct(product=product)


class CreateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        image = graphene.String()
    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, title, image):
        product = Product(title=title, image=image)
        product.save()
        return CreateProduct(product=product)


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
    update_product = UpdateProduct.Field()
    create_product = CreateProduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
