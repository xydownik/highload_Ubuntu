from django.contrib.auth.forms import UserCreationForm

from blog_app.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio']
