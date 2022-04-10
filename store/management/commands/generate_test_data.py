import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Subquery, OuterRef, F, Sum

from store.factories import ProductFactory, OrderFactory, UserFactory, OrderItemFactory
from store.models import Product, Order, OrderItem

USERS_COUNT = 100
PRODUCTS_COUNT = 100
ORDERS_COUNT = 100
MAX_PRODUCTS_PER_ORDER = 10
MAX_QUANTITY_PER_PRODUCT = 10


class Command(BaseCommand):
    # Create a list of names

    @transaction.atomic
    def handle(self, *args, **options):
        User.objects.exclude(username='ruzin').delete()
        Product.objects.all().delete()

        users = [UserFactory() for _ in range(USERS_COUNT)]
        products = [ProductFactory() for _ in range(PRODUCTS_COUNT)]
        orders = [OrderFactory(user=random.choice(users)) for _ in range(ORDERS_COUNT)]

        def get_item(order):
            product = random.choice(products)
            return OrderItemFactory(
                order=order,
                # product=(p := random.choice(products)),
                product=product,
                quantity=random.randint(1, MAX_QUANTITY_PER_PRODUCT),
                price=product.price
            )

        items = [
            [get_item(order) for _ in range(random.randint(1, MAX_PRODUCTS_PER_ORDER))]
            for order in orders
        ]

        items_subquery = OrderItem.objects.filter(order_id=OuterRef('pk')).values('order_id').annotate(
            ttl=Sum(F('price') * F('quantity')))

        Order.objects.update(
            total=Subquery(items_subquery)
        )

        # UPDATE order SET total = (SELECT order_id, sum(price * quantity) as ttl FROM order_item WHERE order_item.order_id = order.id GROUP BY order.id)
