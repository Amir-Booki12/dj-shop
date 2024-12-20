from django.db import transaction
from rest_framework import serializers
from .signals import order_created
from store.models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product


class CollectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Collection
        fields = ['id','title']

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
       model=Product
       fields = ['title','slug','description','unit_price','max_price','collection']
       
    collection = CollectionSerializer()  
    max_price = serializers.SerializerMethodField('round_price')
    
    def round_price(self,obj):
       return obj.unit_price * 100
        
       
       
       
class CreateAndUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
       model=Product
       fields = ['title','slug','description','unit_price','collection']       

class SimpleProductCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id','title','slug','unit_price']
        
class CreateCartItemSerializer(serializers.ModelSerializer):
    
    product_id = serializers.IntegerField()
    
    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']
        try:
            cart_item =CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
                
        except CartItem.DoesNotExist:
          self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data)  
          
           
        return self.instance
       
    
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']
        
 
class UpdateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['quantity']
    
    
                    
class CartItemSerializer(serializers.ModelSerializer):
    
    product = SimpleProductCartItemSerializer()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    
    class Meta:
         model = CartItem
         fields = ['id','product','quantity','total_price']
        

class CartSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
    class Meta:
        model = Cart
        fields = ['id','items','total_price']       


class CustomerSerializer(serializers.ModelSerializer):
    
    user_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','user_id','phone','date_birth','member_ship'] 
        
   
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductCartItemSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','unit_price']   
class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','place_At','customer','payment_status','items']      

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('no cart with the given ID was found')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0 :
            raise serializers.ValidationError('The cart is empty.')
            
        return cart_id
              
    def save(self, **kwargs):   
        with transaction.atomic():
            customer = Customer.objects.get(user_id = self.context['user_id'])
            order= Order.objects.create(customer =customer)   
            
            cart_items = CartItem.objects.select_related('product').filter(cart_id = self.validated_data['cart_id'])
            
            order_item = [
                OrderItem(
                    order = order,
                    product = item.product,
                    quantity = item.quantity,
                    unit_price = item.product.unit_price          
                
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_item)
            Cart.objects.filter(pk=self.validated_data['cart_id']).delete()
            order_created.send_robust(self.__class__,order=order)
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']                    