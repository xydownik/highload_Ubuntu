from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db import connections
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from payments.models import Payment
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import CustomUserCreationForm
from .serializers import *

CACHE_TIMEOUT = 60 * 5

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related('product_set')
    serializer_class = CategorySerializer

# @method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category_id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cache_key = "products_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        cache.set(cache_key, response_data, CACHE_TIMEOUT)
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        cache_key = f"product_{product_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        try:
            product = self.get_object()
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.")
        serializer = self.get_serializer(product)
        response_data = serializer.data

        cache.set(cache_key, response_data, CACHE_TIMEOUT)
        return Response(response_data)

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user_id')
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order_id', 'product_id')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.select_related('user_id')
    serializer_class = ShoppingCartSerializer

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.select_related('cart_id', 'product_id')
    serializer_class = CartItemSerializer

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.using('my_keyspace').all()
    serializer_class = PaymentSerializer

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related('product_id', 'user_id')
    serializer_class = ReviewSerializer


@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class WishlistViewSet(ModelViewSet):
    queryset = Wishlist.objects.select_related('user_id')
    serializer_class = WishlistSerializer

@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class WishlistItemViewSet(ModelViewSet):
    queryset = WishlistItem.objects.select_related('wishlist_id', 'product_id')
    serializer_class = WishlistItemSerializer




def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@ratelimit(key='ip', rate='5/m', method='ALL')
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send response
            return Response({
                "message": "User registered successfully.",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)