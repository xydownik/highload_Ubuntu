from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='user')
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='get_products')
router.register('orders', OrderViewSet, basename='order')
router.register('order-items', OrderItemViewSet, basename='order-item')
router.register('shopping-carts', ShoppingCartViewSet, basename='shopping-cart')
router.register('cart-items', CartItemViewSet, basename='cart-item')
router.register('payments', PaymentViewSet, basename='payment')
router.register('reviews', ReviewViewSet, basename='review')
router.register('wishlists', WishlistViewSet, basename='wishlist')
router.register('wishlist-items', WishlistItemViewSet, basename='wishlist-item'),
urlpatterns = router.urls
urlpatterns += [
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
]
