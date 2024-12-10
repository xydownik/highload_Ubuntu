from django import forms


class PaymentForm(forms.Form):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer')
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS, required=True)
    card_number = forms.CharField(max_length=16, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
    card_expiry = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    card_cvc = forms.CharField(max_length=3, required=False, widget=forms.TextInput(attrs={'placeholder': 'CVC'}))
    paypal_email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'PayPal Email'}))
    bank_account = forms.CharField(max_length=20, required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'Bank Account Number'}))

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method == 'credit_card':
            if not cleaned_data.get('card_number') or not cleaned_data.get('card_expiry') or not cleaned_data.get(
                    'card_cvc'):
                raise forms.ValidationError("All credit card fields must be filled.")

        elif payment_method == 'paypal' and not cleaned_data.get('paypal_email'):
            raise forms.ValidationError("PayPal email is required.")

        elif payment_method == 'bank_transfer' and not cleaned_data.get('bank_account'):
            raise forms.ValidationError("Bank account number is required.")

        return cleaned_data
