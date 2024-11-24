# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'mailApp.mailApp.settings'
#
# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from django.urls import reverse
# from django.core.files.uploadedfile import SimpleUploadedFile
# from mailApp.tasks.models import UploadedFile
# from django.contrib.auth import get_user_model
#
# from mailApp.tasks.views import validate_and_save_file
#
#
# class FileUploadTests(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='password123',
#             email='testuser@example.com'
#         )
#         self.client.login(username='testuser', password='password123')
#
#     def test_file_upload_valid(self):
#         """Test file upload with a valid CSV file"""
#         valid_file = SimpleUploadedFile('test.csv', b"header1,header2\nvalue1,value2")
#         response = self.client.post(reverse('file-upload-url'), {'file': valid_file})
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(UploadedFile.objects.filter(user=self.user).exists())
#
#     def test_file_upload_invalid_extension(self):
#         """Test that only CSV files are allowed"""
#         invalid_file = SimpleUploadedFile('test.txt', b"Some content")
#         response = self.client.post(reverse('file-upload-url'), {'file': invalid_file})
#         self.assertFormError(response, 'form', 'file', 'Only CSV files are allowed.')
#
#     def test_malware_detection(self):
#         """Test that malware is detected during upload"""
#         malicious_file = SimpleUploadedFile('malicious.csv', b"header1,header2\nmalicious_value")
#         with self.assertRaises(ValidationError):
#             validate_and_save_file(malicious_file)
