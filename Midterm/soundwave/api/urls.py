from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('health/', views.health_check, name='health_check')
]
