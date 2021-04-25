import graphene
from my_graphql.ProductType import ProductType
from my_graphql.ProductMutation import UpdateProduct, CreateProduct, DeleteProduct
from products.models import Product


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
    delete_product = DeleteProduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
