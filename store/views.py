
from store.permissions import IsAdminOrReadOnly, ViewCustomerPermission
from store.serializers import CartItemSerializer, CartSerializer, CreateCartItemSerializer, CustomerSerializer, ProductsSerializer,CreateAndUpdateProductSerializer, UpdateCartItemSerializer
from .models import Cart, CartItem, Customer, Product
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
# Create your views here.

class AllProductView(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    permission_classes = [IsAdminOrReadOnly]
   
    
   
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductsSerializer
        else:
            return CreateAndUpdateProductSerializer

    
class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAdminOrReadOnly]
    
    
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
            
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=True,permission_classes=[ViewCustomerPermission])
    def history(self,request,pk):
        return Response('ok')
    
    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        (customer,created) = Customer.objects.get_or_create(user_id =request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method== 'PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
            
            
                    