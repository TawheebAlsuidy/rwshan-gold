from django.test import TestCase
from django.urls import reverse
from contact.models.contact_models import ContactMessage, FAQ


class ContactModelTests(TestCase):
    def setUp(self):
        self.message = ContactMessage.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            subject="Test Subject",
            message="This is a test message"
        )
        
        self.faq = FAQ.objects.create(
            question_en="What is your return policy?",
            question_ar="ما هي سياسة الإرجاع الخاصة بك؟",
            answer_en="Our return policy is 30 days.",
            answer_ar="سياسة الإرجاع الخاصة بنا هي 30 يومًا.",
            order=1
        )
    
    def test_contact_message_creation(self):
        self.assertEqual(str(self.message), "John Doe - Test Subject")
    
    def test_faq_creation(self):
        self.assertEqual(str(self.faq), "What is your return policy?")


class ContactViewTests(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question_en="What is your return policy?",
            question_ar="ما هي سياسة الإرجاع الخاصة بك؟",
            answer_en="Our return policy is 30 days.",
            answer_ar="سياسة الإرجاع الخاصة بنا هي 30 يومًا.",
            order=1
        )
    
    def test_contact_view(self):
        response = self.client.get(reverse('contact:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What is your return policy?")
    
    def test_faq_view(self):
        response = self.client.get(reverse('contact:faq'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What is your return policy?")