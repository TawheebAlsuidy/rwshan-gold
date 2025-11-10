# contact/management/commands/test_real_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test real email sending'

    def handle(self, *args, **options):
        try:
            send_mail(
                subject='اختبار إرسال البريد - Rwshan Gold',
                message='هذه رسالة اختبار من نظام Rwshan Gold Company',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['alsuidytauheeb@gmail.com'],  # استبدل بإيميلك
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('✅ تم إرسال رسالة الاختبار بنجاح!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ خطأ في الإرسال: {e}'))