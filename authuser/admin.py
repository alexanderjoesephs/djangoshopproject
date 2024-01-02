from django.contrib import admin
from .models import User, Product, Cart, CartItem, Review

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)


