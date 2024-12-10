from django.urls import path
from .import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('prducts/', views.product_list, name='products'),
    path('products/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.order_history, name='order_history'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('reviews/<int:product_id>/', views.add_review, name='add_review'),
]
