from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal')])
    amount_paid = forms.DecimalField(max_digits=10, decimal_places=2)
