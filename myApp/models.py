from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, 
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True, null=True
    )

    def __str__(self):
        return self.usernamepyt

CATEGORY_CHOICES = [
    ('MEN', 'Men'),
    ('WOMEN', 'Women'),
    ('KIDS', 'Kids'),
    ('ACCESSORIES', 'Accessories'),
]

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category_type = models.CharField(max_length=20, default='shirt')

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    category_choices = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='shirt')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField('myApp.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, default="Unknown")
    last_name = models.CharField(max_length=100, default="Unknown")
    email = models.EmailField(unique=True, default='default@example.com')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.customer}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.cart}"

User = get_user_model()  # Dynamically get the custom user model

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='wishlist_items')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
