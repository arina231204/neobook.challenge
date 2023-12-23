from django.db import models
from django.contrib.sessions.models import Session

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    quantity_available = models.IntegerField()
    image = models.ImageField(upload_to='images/')


    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.session})"

class Order(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"