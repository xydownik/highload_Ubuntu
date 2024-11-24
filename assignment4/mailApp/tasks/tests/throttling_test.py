# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient
# from django.test import TestCase
#
# class RoleBasedThrottleTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='password123',
#             email='testuser@example.com'
#         )
#
#     def test_user_throttling(self):
#         """Test that user throttling works as expected"""
#         self.client.login(username='testuser', password='password123')
#         response = self.client.get('/some-api-endpoint/')  # Replace with actual endpoint
#         self.assertEqual(response.status_code, 200)
#
#         # Simulate a large number of requests for throttling
#         for _ in range(10):
#             response = self.client.get('/some-api-endpoint/')  # Replace with actual endpoint
#             if _ < 5:
#                 self.assertEqual(response.status_code, 200)
#             else:
#                 self.assertEqual(response.status_code, 429)  # Too many requests
