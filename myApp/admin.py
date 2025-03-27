from django.contrib import admin
from .models import Category, Brand, CustomUser, Item, Customer

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Item)
admin.site.register(Customer)
