import factory.fuzzy

from store.models import Product, Order, OrderItem
from django.contrib.auth.models import User


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('sentence', nb_words=3, variable_nb_words=True)
    description = factory.Faker('sentence', nb_words=100, variable_nb_words=True)
    price = factory.fuzzy.FuzzyDecimal(0.10, 9999.99)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name', locale='ru_RU',)
    last_name = factory.Faker('last_name', locale='ru_RU')


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    products = factory.RelatedFactory(ProductFactory, 'order')
    address = factory.Faker('address', locale='ru_RU')
    total = factory.fuzzy.FuzzyDecimal(0.10, 99999.99)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 10)
    price = factory.fuzzy.FuzzyDecimal(0.10, 99999.99)
