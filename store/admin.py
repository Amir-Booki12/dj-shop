from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem, Customer, Product,Collection

admin.site.register(Product)
admin.site.register(Collection)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Customer)
