import profile

from django.urls import path, include

from .views import *

urlpatterns = [
    path('send-email/', send_email_view, name='send_email'),
    path('emails/', email_list, name='email_list' ),
    path('profile/', ProfileView.as_view(), name='profile'),
]