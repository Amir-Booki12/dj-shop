
from store.serializers import CartItemSerializer, CartSerializer, CreateCartItemSerializer, ProductsSerializer,CreateAndUpdateProductSerializer, UpdateCartItemSerializer
from .models import Cart, CartItem, Product
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
# Create your views here.

class AllProductView(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductsSerializer
        else:
            return CreateAndUpdateProductSerializer

    
class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductsSerializer
        else:
            return CreateAndUpdateProductSerializer

        
class CartViewSet(CreateModelMixin,RetrieveModelMixin,GenericViewSet) :
    queryset = Cart.objects.all()
    serializer_class = CartSerializer       
        

class CartItemViewSet(ModelViewSet):
    
    http_method_names = ['get','post','patch','delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs.get('cart_pk'))
            
        