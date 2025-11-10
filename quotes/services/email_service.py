# quotes/services/email_service.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import re

def strip_css(html_content):
    """إزالة محتوى CSS من النص العادي"""
    # إزالة محتوى الـ style
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
    # إزالة محتوى الـ head
    html_content = re.sub(r'<head[^>]*>.*?</head>', '', html_content, flags=re.DOTALL)
    # إزالة جميع الوسوم
    text_content = strip_tags(html_content)
    # تنظيف المسافات الزائدة
    text_content = re.sub(r'\n\s*\n', '\n\n', text_content)
    return text_content.strip()

def send_quote_notification(quote_request):
    """
    إرسال إشعار بعرض سعر جديد إلى بريد الموقع
    """
    subject = _('New Quote Request - {}').format(quote_request.quote_id)
    
    # تحضير البيانات للقالب
    context = {
        'quote': quote_request,
        'company_name': 'Rwshan Gold Company',
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:7723'
    }
    
    # تحميل القالب HTML
    html_content = render_to_string('quotes/emails/new_quote_notification.html', context)
    text_content = strip_css(html_content)
    
    # إنشاء الرسالة
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.COMPANY_EMAIL],
        reply_to=[quote_request.email]
    )
    
    # إضافة النسخة HTML
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send(fail_silently=False)
        print(f"✅ Email sent successfully to {settings.COMPANY_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_quote_confirmation(quote_request):
    """
    إرسال تأكيد إلى العميل
    """
    subject = _('Your Quote Request Confirmation - {}').format(quote_request.quote_id)
    
    context = {
        'quote': quote_request,
        'company_name': 'Rwshan Gold Company',
        'contact_email': settings.COMPANY_EMAIL
    }
    
    html_content = render_to_string('quotes/emails/quote_confirmation.html', context)
    text_content = strip_css(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[quote_request.email],
        reply_to=[settings.COMPANY_EMAIL]
    )
    
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send(fail_silently=False)
        print(f"✅ Confirmation email sent to {quote_request.email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send confirmation email: {e}")
        return False