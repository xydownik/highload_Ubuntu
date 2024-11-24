from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Email, UploadedFile
from django import forms
from .models import UserProfile
from django.utils.html import escape

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['subject', 'body','recipient']

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'email', 'telegram_account', 'description', 'UIN']

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        return escape(description)

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if not name.isalnum():
            raise forms.ValidationError("Name should contain only letters and numbers.")
        return name

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV files are allowed.")
        return file