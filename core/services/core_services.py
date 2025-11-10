from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def send_contact_notification(contact_data):
    subject = _('New Contact Message from Rwshan Gold Website')
    message = f"""
    Name: {contact_data['name']}
    Email: {contact_data['email']}
    Subject: {contact_data['subject']}
    Message: {contact_data['message']}
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )