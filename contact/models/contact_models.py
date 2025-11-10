from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class ContactMessage(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20)
    subject = models.CharField(_("Subject"), max_length=200)
    message = models.TextField(_("Message"))
    is_read = models.BooleanField(_("Is Read"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class FAQ(TranslatableModel):
    translations = TranslatedFields(
        question = models.TextField(_("Question")),
        answer = models.TextField(_("Answer")),
    )
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ['order']
    
    def __str__(self):
        return self.safe_translation_getter('question', any_language=True)