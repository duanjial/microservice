import graphene
from my_graphql.ProductType import ProductType
from products.models import Product


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
