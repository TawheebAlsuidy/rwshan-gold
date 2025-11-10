from django.views.generic import TemplateView, CreateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string, TemplateDoesNotExist
from django.utils.translation import gettext_lazy as _
import logging

from contact.models.contact_models import ContactMessage, FAQ
from contact.forms.contact_forms import ContactForm

logger = logging.getLogger(__name__)

class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact:success')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        try:
            # Send email notification
            email_sent = self.send_contact_email(self.object)
            
            if email_sent:
                messages.success(self.request, _('Your message has been sent successfully! We will contact you soon.'))
                logger.info(f"Contact message sent successfully from {self.object.email}")
            else:
                messages.warning(self.request, _('Your message was saved but there was an issue sending the email notification. We will still contact you soon.'))
                logger.warning(f"Contact message saved but email failed for {self.object.email}")
                
        except Exception as e:
            messages.warning(self.request, _('Your message was saved but there was an issue sending the email notification. We will still contact you soon.'))
            logger.error(f"Error in contact form: {str(e)}")
        
        return response
    
    def send_contact_email(self, contact_message):
        """Send email notification for new contact message"""
        try:
            subject = f"New Contact Message: {contact_message.subject}"
            
            # HTML email content
            context = {
                'name': contact_message.name,
                'email': contact_message.email,
                'phone': contact_message.phone,
                'subject': contact_message.subject,
                'message': contact_message.message,
                'created_at': contact_message.created_at,
            }
            
            try:
                html_message = render_to_string('contact/email/contact_notification.html', context)
                plain_message = render_to_string('contact/email/contact_notification.txt', context)
            except TemplateDoesNotExist as e:
                logger.error(f"Template not found: {e}")
                # Fallback to simple email
                plain_message = f"""
                New Contact Message from {contact_message.name}
                
                Email: {contact_message.email}
                Phone: {contact_message.phone}
                Subject: {contact_message.subject}
                
                Message:
                {contact_message.message}
                
                Received at: {contact_message.created_at}
                """
                html_message = None
            
            # Send email to company with proper encoding
            self.send_email_safely(
                subject=subject,
                plain_message=plain_message,
                recipient_list=[settings.CONTACT_EMAIL],
                html_message=html_message
            )
            
            logger.info(f"Notification email sent to {settings.CONTACT_EMAIL}")
            
            # Send confirmation email to user
            self.send_confirmation_email(contact_message)
            
            return True
            
        except BadHeaderError:
            logger.error("Invalid header found in email")
            return False
        except Exception as e:
            logger.error(f"Error sending contact email: {str(e)}")
            return False
    
    def send_confirmation_email(self, contact_message):
        """Send confirmation email to the user"""
        try:
            subject = _("Thank you for contacting Rwshan Gold Company")
            
            context = {
                'name': contact_message.name,
                'subject': contact_message.subject,
            }
            
            try:
                html_message = render_to_string('contact/email/confirmation_email.html', context)
                plain_message = render_to_string('contact/email/confirmation_email.txt', context)
            except TemplateDoesNotExist as e:
                logger.error(f"Confirmation template not found: {e}")
                # Fallback to simple email
                plain_message = f"""
                Thank you for contacting Rwshan Gold Company!
                
                Hello {contact_message.name},
                
                We have received your message regarding "{contact_message.subject}" and will respond within 24 hours.
                
                Best regards,
                The Rwshan Gold Company Team
                """
                html_message = None
            
            self.send_email_safely(
                subject=subject,
                plain_message=plain_message,
                recipient_list=[contact_message.email],
                html_message=html_message
            )
            
            logger.info(f"Confirmation email sent to {contact_message.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending confirmation email: {str(e)}")
            return False
    
    def send_email_safely(self, subject, plain_message, recipient_list, html_message=None):
        """Send email with proper encoding handling"""
        try:
            # Ensure proper encoding for the subject
            subject = subject.encode('utf-8', 'ignore').decode('utf-8')
            
            # Ensure proper encoding for the message content
            if isinstance(plain_message, str):
                plain_message = plain_message.encode('utf-8', 'ignore').decode('utf-8')
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
        except UnicodeEncodeError as e:
            logger.error(f"Unicode encoding error: {e}")
            # Fallback: send without special characters
            subject = "New Contact Message"
            plain_message = "A new contact message has been received. Please check the admin panel for details."
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=None,
                fail_silently=False,
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True)[:5]
        return context


class ContactSuccessView(TemplateView):
    template_name = 'contact/success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Message Sent Successfully")
        return context


class FAQListView(ListView):
    model = FAQ
    template_name = 'contact/faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Frequently Asked Questions")
        return context