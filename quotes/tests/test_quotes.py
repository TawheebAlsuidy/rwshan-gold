from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from quotes.models.quote_models import QuoteRequest
from products.models import ProductCategory, Product, FabricOption, ColorOption


class QuoteModelTests(TestCase):
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
        
        self.quote = QuoteRequest.objects.create(
            user=self.user,
            product=self.product,
            fabric=self.fabric,
            color=self.color,
            quantity=10,
            logo_complexity='simple',
            company_name='Test Company',
            contact_person='John Doe',
            email='john@example.com',
            phone='1234567890'
        )
    
    def test_quote_request_creation(self):
        self.assertEqual(str(self.quote), "Test Company - Test Product")
        self.assertEqual(self.quote.get_quantity_discount(), 0)
        self.assertEqual(self.quote.get_logo_complexity_fee(), 10)
        self.assertEqual(self.quote.calculate_price(), 1100.00)


class QuoteViewTests(TestCase):
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
    
    def test_quote_calculator_view(self):
        response = self.client.get(reverse('quotes:calculator'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Price Calculator")
    
    def test_quote_request_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'product': self.product.id,
            'fabric': self.fabric.id,
            'color': self.color.id,
            'quantity': 10,
            'logo_complexity': 'simple',
            'company_name': 'Test Company',
            'contact_person': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'notes': 'Test notes'
        }
        
        response = self.client.post(reverse('quotes:request'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertEqual(QuoteRequest.objects.count(), 1)