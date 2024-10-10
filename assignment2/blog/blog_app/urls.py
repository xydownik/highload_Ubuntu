from django.urls import path, include

from . import views
from accounts.views import *

urlpatterns = [
    path('posts/', views.post_list_view, name='post_list'  ),
    path('post_detail/<int:id>/', views.post_detail_view, name='post_detail'),
    path('posts/new/', views.create_post, name='create_post'),
    path('posts/<int:id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('health/', views.health_check, name='health_check')
]