# from concurrent.futures import ThreadPoolExecutor
# from django.test import TestCase
# from ..models import UploadedFile
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.urls import reverse
# from django.contrib.auth import get_user_model
#
# class ConcurrentFileUploadTests(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='password123',
#             email='testuser@example.com'
#         )
#         self.client.login(username='testuser', password='password123')
#
#     def test_concurrent_uploads(self):
#         """Test that multiple file uploads can happen concurrently"""
#         valid_file = SimpleUploadedFile('test.csv', b"header1,header2\nvalue1,value2")
#         def upload_file():
#             self.client.post(reverse('file-upload-url'), {'file': valid_file})
#
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             futures = [executor.submit(upload_file) for _ in range(5)]
#             for future in futures:
#                 future.result()
#
#         self.assertEqual(UploadedFile.objects.filter(user=self.user).count(), 5)
