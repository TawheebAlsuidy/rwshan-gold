from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.urls import reverse

class Client(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='clients/logos/')
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")


class Testimonial(TranslatableModel):
    client_name_ar = models.CharField(_("Arabic Client Name"), max_length=100)
    client_name_en = models.CharField(_("English Client Name"), max_length=100)
    company_ar = models.CharField(_("Arabic Company"), max_length=100)
    company_en = models.CharField(_("English Company"), max_length=100)
    translations = TranslatedFields(
        content=models.TextField(_("Content")),
    )
    video_url = models.URLField(_("Video URL"), blank=True)
    image = models.ImageField(_("Client Image"), upload_to='testimonials/', blank=True)
    is_featured = models.BooleanField(_("Is Featured"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ['-created_at']
    
    @property
    def client_name(self):
        from django.utils.translation import get_language
        if get_language() == 'ar':
            return self.client_name_ar
        return self.client_name_en
    
    @property
    def company(self):
        from django.utils.translation import get_language
        if get_language() == 'ar':
            return self.company_ar
        return self.company_en

    def get_absolute_url(self):
        return reverse('testimonials:list')


class ClientPartner(TranslatableModel):
    name_ar = models.CharField(_("Arabic Name"), max_length=100)
    name_en = models.CharField(_("English Name"), max_length=100)
    logo = models.ImageField(_("Logo"), upload_to='client_logos/')
    website_url = models.URLField(_("Website URL"), blank=True)
    is_featured = models.BooleanField(_("Is Featured"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Client Partner")
        verbose_name_plural = _("Client Partners")
        ordering = ['-created_at']
    
    @property
    def name(self):
        from django.utils.translation import get_language
        if get_language() == 'ar':
            return self.name_ar
        return self.name_en

    def get_absolute_url(self):
        return reverse('testimonials:clients')


class CaseStudy(TranslatableModel):
    title_ar = models.CharField(_("Arabic Title"), max_length=200)
    title_en = models.CharField(_("English Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    client = models.ForeignKey(ClientPartner, on_delete=models.CASCADE, related_name='case_studies')
    translations = TranslatedFields(
        excerpt=models.TextField(_("Excerpt")),
        content=models.TextField(_("Content")),
    )
    before_image = models.ImageField(_("Before Image"), upload_to='case_studies/')
    after_image = models.ImageField(_("After Image"), upload_to='case_studies/')
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Case Study")
        verbose_name_plural = _("Case Studies")
        ordering = ['-created_at']
    
    @property
    def title(self):
        from django.utils.translation import get_language
        if get_language() == 'ar':
            return self.title_ar
        return self.title_en

    def get_absolute_url(self):
        return reverse('testimonials:case_study_detail', kwargs={'case_study_slug': self.slug})