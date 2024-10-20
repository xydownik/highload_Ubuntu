from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import Product
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import Order
from soundwave.tasks import process_order


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()
    def get_queryset(self):
        queryset = Product.objects.all()

        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        order_by_name = self.request.query_params.get('order_by_name', None)
        if order_by_name == 'asc':
            queryset = queryset.order_by('name')
        elif order_by_name == 'desc':
            queryset = queryset.order_by('-name')

        queryset = queryset.select_related('category')

        return queryset
    def list(self, request, *args, **kwargs):
        cache_key =  f"products_list_{request.query_params.get('name', '')}_{request.query_params.get('category', '')}_{request.query_params.get('order_by_name', '')}"
        cached_products = cache.get(cache_key)
        if cached_products:
            return Response(cached_products)

        response = super().list(request, *args, **kwargs)
        cache.set('products_list', response.data, timeout=60 * 15)
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete('products_list')
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete('products_list')
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete('products_list')
        return response

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_orders_cache_key = f"user_orders_{self.request.user.id}"
        cached_orders = cache.get(user_orders_cache_key)

        if cached_orders:
            return cached_orders

        queryset = Order.objects.filter(user=self.request.user) \
            .prefetch_related('orderItems__product') \
            .select_related('user')

        cache.set(user_orders_cache_key, queryset, timeout=60 * 15)  # Cache for 15 minutes
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete(f"user_orders_{self.request.user.id}")
        return response

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        process_order.delay(order.id)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete(f"user_orders_{self.request.user.id}")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete(f"user_orders_{self.request.user.id}")
        return response
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_order_items_cache_key = f"user_order_items_{self.request.user.id}"
        cached_order_items = cache.get(user_order_items_cache_key)

        if cached_order_items:
            return cached_order_items

        queryset = OrderItem.objects.filter(user=self.request.user).select_related('product', 'user')

        cache.set(user_order_items_cache_key, queryset, timeout=60*15)  # Cache for 15 minutes
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete(f"user_order_items_{self.request.user.id}")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete(f"user_order_items_{self.request.user.id}")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete(f"user_order_items_{self.request.user.id}")
        return response



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)