import profile

from django.urls import path, include

from .views import *

urlpatterns = [
    path('send-email/', send_email_view, name='send_email'),
    path('emails/', email_list, name='email_list' ),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/my-emails/', UserEmailsView.as_view(), name='my_emails'),
    path('profile/my-emails/<int:id>', UserEmailsView.as_view(), name='email'),
    path('upload/', upload_file_view, name='upload_file_view'),
    path('upload/success/', upload_success_view, name='upload_success'),
    path('progress/<int:file_id>/', file_progress_view, name='file_progress'),

]