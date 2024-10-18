from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import Product
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        # Override the list method to filter by the logged-in user
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")  # Simple query to test DB connection
    except Exception as e:
        return JsonResponse({'status': 'error', 'database': str(e)}, status=503)

        # Check cache
    try:
        cache.set('health_check', 'working', 1)
        if cache.get('health_check') != 'working':
            raise Exception('Cache not working')
    except Exception as e:
        return JsonResponse({'status': 'error', 'cache': str(e)}, status=503)

        # Everything is OK
    return JsonResponse({'status': 'ok'}, status=200)
