from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    owner = models.ForeignKey(User, related_name='stores', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    stores = models.ManyToManyField('Store', related_name='products')

    class Meta:
        permissions = [
            ("change_stock", "Can update stock quantity"),
            ("change_price", "Can update product price"),
        ]

    def is_low_stock(self):
        return self.quantity < 5  # Example threshold for low stock

    def __str__(self):
        return self.name