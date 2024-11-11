from django.urls import path

from .views import *

urlpatterns = [
    path('send-email/', send_email_view, name='send_email'),
    path('emails/', email_list, name='email_list' ),
    path('emails/<int:pk>/', email_detail, name='email_detail')

]