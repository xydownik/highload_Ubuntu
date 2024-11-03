from django.urls import path

from .views import KeyValueStoreView
from . import views
urlpatterns = [
    path('key-value/', KeyValueStoreView.as_view()),
    path('key-value/<str:key>/', KeyValueStoreView.as_view()),
    path('write/', views.KeyValueStore, name='write_view'),
    path('read/<str:key>/', views.KeyValueStore, name='read_view'),
    path('test-logging/', views.test_logging, name='test_logging'),
]
