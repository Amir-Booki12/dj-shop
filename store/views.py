
from store.permissions import IsAdminOrReadOnly, ViewCustomerPermission
from store.serializers import CartItemSerializer, CartSerializer, CreateCartItemSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductsSerializer,CreateAndUpdateProductSerializer, UpdateCartItemSerializer, UpdateOrderSerializer
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from .models import Cart, CartItem, Customer, Order, OrderItem, Product
from django.shortcuts import get_object_or_404

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
        customer = Customer.objects.get(user_id =request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method== 'PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
            

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
        
    def get(self,request):
        user = request.user 
        if user.is_staff:
            order = Order.objects.all()       
        else:
            customer_id = Customer.objects.only('id').get(user_id=user.id)
            order = Order.objects.filter(customer_id=customer_id)      
        serializer = OrderSerializer(instance=order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)            
     
    def post(self,request):
        serializer = CreateOrderSerializer(data=request.data,context={'user_id':request.user.id})
        serializer.is_valid(raise_exception=True)
        order  = serializer.save()
        serializer = OrderSerializer(order)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)                
 

class OrderDetailView(APIView):
    
    permission_classes= [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get(self,request,pk):
        order = get_object_or_404(Order,pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,pk):
        order = get_object_or_404(Order,pk=pk)
        if OrderItem.objects.filter(order=order):
            return Response('you cant remove order when orderItem existing')
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self,request,pk):
        order = get_object_or_404(Order,pk=pk)
        serializer = UpdateOrderSerializer(instance=order,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
        
        
        
        
            