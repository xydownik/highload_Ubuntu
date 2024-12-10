# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.view_order, name='view_order'),
    path('pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('order_success/', views.order_success, name='order_success'),
]
