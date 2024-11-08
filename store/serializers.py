from rest_framework import serializers

from store.models import Cart, CartItem, Collection, Customer, Product


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
        
          