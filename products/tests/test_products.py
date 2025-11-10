from django.test import TestCase
from django.urls import reverse
from products.models.product_models import ProductCategory, Product


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(
            name_en="Test Category",
            name_ar="فئة الاختبار",
            slug="test-category"
        )
        self.product = Product.objects.create(
            name_en="Test Product",
            name_ar="منتج اختبار",
            slug="test-product",
            category=self.category,
            base_price=100.00
        )
    
    def test_product_creation(self):
        self.assertEqual(str(self.product), "Test Product")
    
    def test_category_creation(self):
        self.assertEqual(str(self.category), "Test Category")


class ProductViewTests(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(
            name_en="Test Category",
            name_ar="فئة الاختبار",
            slug="test-category"
        )
        self.product = Product.objects.create(
            name_en="Test Product",
            name_ar="منتج اختبار",
            slug="test-product",
            category=self.category,
            base_price=100.00
        )
    
    def test_category_list_view(self):
        response = self.client.get(reverse('products:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")
    
    def test_category_detail_view(self):
        response = self.client.get(reverse('products:category_detail', kwargs={'category_slug': 'test-category'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
    
    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', kwargs={'product_slug': 'test-product'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")