from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models.blog_models import Post, PostCategory


class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = PostCategory.objects.create(
            name_en="Test Category",
            name_ar="فئة الاختبار",
            slug="test-category"
        )
        
        self.post = Post.objects.create(
            title_en="Test Post",
            title_ar="منشور اختبار",
            slug="test-post",
            author=self.user,
            category=self.category,
            excerpt="This is a test post",
            content="This is the content of the test post",
            status='published'
        )
    
    def test_post_creation(self):
        self.assertEqual(str(self.post), "Test Post")
    
    def test_category_creation(self):
        self.assertEqual(str(self.category), "Test Category")


class BlogViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = PostCategory.objects.create(
            name_en="Test Category",
            name_ar="فئة الاختبار",
            slug="test-category"
        )
        
        self.post = Post.objects.create(
            title_en="Test Post",
            title_ar="منشور اختبار",
            slug="test-post",
            author=self.user,
            category=self.category,
            excerpt="This is a test post",
            content="This is the content of the test post",
            status='published'
        )
    
    def test_post_list_view(self):
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
    
    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:detail', kwargs={'post_slug': 'test-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
    
    def test_category_post_list_view(self):
        response = self.client.get(reverse('blog:category_list', kwargs={'category_slug': 'test-category'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")