# from django.test import TestCase
# from django.urls import reverse
#
#
# class UserRegistrationTests(TestCase):
#     def test_duplicate_email(self):
#         """Test that duplicate email addresses are not allowed"""
#         user_data = {
#             'username': 'testuser1',
#             'email': 'testuser@example.com',
#             'password1': 'password123',
#             'password2': 'password123',
#         }
#         self.client.post(reverse('register'), user_data)
#         response = self.client.post(reverse('register'), user_data)
#         self.assertFormError(response, 'form', 'email', 'This email address is already registered.')
