# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from unittest.mock import patch
# from tasks.models import Email
#
#
# class SendEmailViewTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='password123')
#         self.client.login(username='testuser', password='password123')
#         self.url = reverse('send_email')
#
#     @patch('tasks.views.send_email_task.delay')
#     def test_send_email_valid(self, mock_send_email_task):
#         data = {
#             'subject': 'Test Subject',
#             'body': 'Test Body',
#             'recipient': 'recipient@example.com',
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(Email.objects.filter(subject='Test Subject').exists())
#         mock_send_email_task.assert_called_once()
#
#     def test_send_email_unauthenticated(self):
#         self.client.logout()
#         response = self.client.post(self.url, {'subject': 'Test', 'body': 'Test body', 'recipient': 'test@example.com'})
#         self.assertEqual(response.status_code, 302)  # Redirects to login
#
#
# class EmailListViewTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='password123')
#         self.email = Email.objects.create(subject="Test Subject", body="Test Body", recipient="recipient@example.com")
#
#     def test_email_list_view(self):
#         self.client.login(username='testuser', password='password123')
#         response = self.client.get(reverse('email_list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Test Subject")
