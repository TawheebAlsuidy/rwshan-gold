from django.test import TestCase
from django.urls import reverse
from testimonials.models.testimonial_models import Testimonial, ClientPartner, CaseStudy


class TestimonialModelTests(TestCase):
    def setUp(self):
        self.testimonial = Testimonial.objects.create(
            client_name_ar="عميل اختبار",
            client_name_en="Test Client",
            company_ar="شركة اختبار",
            company_en="Test Company",
            content_ar="هذا هو محتوى الشهادة",
            content_en="This is the testimonial content",
            is_featured=True
        )
    
    def test_testimonial_creation(self):
        self.assertEqual(self.testimonial.client_name, "Test Client")
        self.assertEqual(self.testimonial.company, "Test Company")
        self.assertEqual(self.testimonial.content, "This is the testimonial content")


class ClientPartnerModelTests(TestCase):
    def setUp(self):
        self.client = ClientPartner.objects.create(
            name_ar="شريك اختبار",
            name_en="Test Partner",
            website_url="https://example.com",
            is_featured=True
        )
    
    def test_client_partner_creation(self):
        self.assertEqual(self.client.name, "Test Partner")


class TestimonialViewTests(TestCase):
    def setUp(self):
        self.testimonial = Testimonial.objects.create(
            client_name_ar="عميل اختبار",
            client_name_en="Test Client",
            company_ar="شركة اختبار",
            company_en="Test Company",
            content_ar="هذا هو محتوى الشهادة",
            content_en="This is the testimonial content",
            is_featured=True
        )
        
        self.client_partner = ClientPartner.objects.create(
            name_ar="شريك اختبار",
            name_en="Test Partner",
            website_url="https://example.com",
            is_featured=True
        )
    
    def test_testimonial_list_view(self):
        response = self.client.get(reverse('testimonials:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Client")
    
    def test_client_partner_list_view(self):
        response = self.client.get(reverse('testimonials:clients'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Partner")