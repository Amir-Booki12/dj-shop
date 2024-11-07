from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem, Product,Collection

admin.site.register(Product)
admin.site.register(Collection)
admin.site.register(Cart)
admin.site.register(CartItem)
