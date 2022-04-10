from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.price}'


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField('Product', through='OrderItem')

    def __str__(self):
        return f'{self.pk} - {self.user.first_name} {self.user.last_name} - {self.total}'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
