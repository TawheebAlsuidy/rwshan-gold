from django.test import TestCase
from django.urls import reverse
from core.models.core_models import GeneralSetting


class CoreModelTests(TestCase):
    def test_general_setting_creation(self):
        setting = GeneralSetting.objects.create(
            key='test_key',
            value='test_value',
            description='Test description'
        )
        self.assertEqual(str(setting), 'test_key')


class CoreViewTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_page_status_code(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)