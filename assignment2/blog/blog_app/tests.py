from django.test import TestCase

# Create your tests here.
from .models import Post, Comment, User

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Test Comment')

    def test_post_with_comments(self):
        posts_with_comments = Post.objects.prefetch_related('comments').select_related('author')
        self.assertEqual(posts_with_comments.count(), 1)
        self.assertEqual(posts_with_comments.first().comments.count(), 1)
