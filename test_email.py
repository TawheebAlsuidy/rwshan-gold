# إنشاء ملف test_email.py في المجلد الرئيسي للتجربة
import os
import django
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rwshan_gold.settings.development')
django.setup()

def test_email():
    try:
        send_mail(
            'Test Email from Django',
            'This is a test email to check SMTP settings.',
            'malukamagairha73@gmail.com',
            ['alsuidytauheeb@gmail.com'],
            fail_silently=False,
        )
        print("✅ Test email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")

if __name__ == "__main__":
    test_email()