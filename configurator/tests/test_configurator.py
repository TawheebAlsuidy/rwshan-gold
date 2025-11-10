from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from configurator.models.configurator_models import UniformDesign
from products.models.product_models import ProductCategory, Product, FabricOption, ColorOption


class ConfiguratorModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
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
        
        self.fabric = FabricOption.objects.create(
            name_en="Cotton",
            name_ar="قطن",
            price_modifier=10.00
        )
        
        self.color = ColorOption.objects.create(
            name_en="Blue",
            name_ar="أزرق",
            hex_code="#0000FF"
        )
        
        self.design = UniformDesign.objects.create(
            user=self.user,
            product=self.product,
            fabric=self.fabric,
            color=self.color
        )
    
    def test_uniform_design_creation(self):
        self.assertEqual(str(self.design), "Test Product - testuser")
        self.assertEqual(self.design.get_total_price(), 110.00)


class ConfiguratorViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
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
        
        self.fabric = FabricOption.objects.create(
            name_en="Cotton",
            name_ar="قطن",
            price_modifier=10.00
        )
        
        self.color = ColorOption.objects.create(
            name_en="Blue",
            name_ar="أزرق",
            hex_code="#0000FF"
        )
    
    def test_configurator_start_view(self):
        response = self.client.get(reverse('configurator:start'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")
    
    def test_configurator_step1_view(self):
        response = self.client.get(reverse('configurator:step1'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Customize Your Uniform")