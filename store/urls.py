from django.urls import path
from . import views
from rest_framework_nested import routers

app_name = 'store'

router = routers.DefaultRouter()
router.register('carts',views.CartViewSet,basename='carts')

cart_item_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_item_router.register('items',views.CartItemViewSet,basename='cart_items')

urlpatterns = [
    path('products/',views.AllProductView.as_view(),name='all_products'),
    path('products/<int:id>/',views.ProductDetails.as_view(),name='product_detail'),
]

urlpatterns += router.urls + cart_item_router.urls