from django.db import models
from uuid import uuid4
# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
   
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300)
    description = models.TextField(blank=True,null=True)
    unit_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT,related_name='products')
    
    def __str__(self):
        return self.title
    
class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='products')
    quantity = models.PositiveSmallIntegerField()


    