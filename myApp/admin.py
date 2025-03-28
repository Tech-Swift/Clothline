from django.contrib import admin
from .models import Cart, CartItem, Category, Brand, CustomUser, Item, Customer

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)

