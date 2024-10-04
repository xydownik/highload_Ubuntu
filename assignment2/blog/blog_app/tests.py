import os
import django
from django.test import TestCase

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

# Ensure that Django setup is called before importing models
django.setup()

# Import models
from .models import Post, Comment, User

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Test Comment')

    def test_post_with_comments(self):
        posts_with_comments = Post.objects.prefetch_related('comments').select_related('author')
        self.assertEqual(posts_with_comments.count(), 2)
        self.assertEqual(posts_with_comments[1].comments.count(), 1)

# from django.core.cache import cache
#
# # Set a cache value
# cache.set('my_key', 'my_value', timeout=60)
#
# # Get the cached value
# value = cache.get('my_key')
# print(value)  # Should print 'my_value'