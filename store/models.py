from django.db import models
from uuid import uuid4
from django.conf import settings
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
    

class Customer(models.Model):
    GOLD = 'G'
    BRONZE = 'B'
    SILVER = 'S'
 
    MEMBER_SHIP_CHOICES = [
        (GOLD, 'Gold'),
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
    ]
    phone = models.CharField(max_length=12)
    date_birth = models.DateField(null=True,blank=True)
    member_ship = models.CharField(max_length=1,choices=MEMBER_SHIP_CHOICES,default=SILVER)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='customers')
    
    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name}'
    
    class Meta:
        permissions = [
            ('view_history' , 'can view history')
        ]
 
 
 
 
    
class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='products')
    quantity = models.PositiveSmallIntegerField()


class Order(models.Model):
    PENDING = 'P'
    COMPLETE = 'C'
    FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES =[
        (PENDING,'pending'),
        (COMPLETE,'complete'),
        (FAILED,'failed'),
    ]
    
    place_At = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='orders')
    
    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.IntegerField()
