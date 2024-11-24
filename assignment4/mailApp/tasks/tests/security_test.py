# from django.test import TestCase
# from tasks.forms import UserProfileForm
# from tasks.models import UserProfile
#
# class SecurityTests(TestCase):
#     def test_xss_protection_in_description(self):
#         """Test that XSS input in description is sanitized"""
#         xss_content = '<script>alert("XSS")</script>'
#         form_data = {
#             'name': 'Test User',
#             'age': 25,
#             'email': 'testuser@example.com',
#             'telegram_account': 'http://example.com',
#             'description': xss_content,
#             'UIN': '123456789012'
#         }
#         form = UserProfileForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         user_profile = form.save()
#         self.assertNotIn(xss_content, user_profile.description)  # Ensure script tags are sanitized
#         self.assertIn('alert("XSS")', user_profile.description)  # Should be encoded, not executed
