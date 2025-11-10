from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
from parler.models import TranslatableModel, TranslatedFields


class PostCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("Name"), max_length=100),
        description = models.TextField(_("Description"), blank=True),
    )
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Post Category")
        verbose_name_plural = _("Post Categories")

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Post(TranslatableModel):
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
    ]

    translations = TranslatedFields(
        title = models.CharField(_("Title"), max_length=200),
        excerpt = models.TextField(_("Excerpt"), max_length=300),
        content = models.TextField(_("Content")),
        meta_description = models.TextField(_("Meta Description"), max_length=160, blank=True),
    )
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='posts')
    featured_image = models.ImageField(_("Featured Image"), upload_to='blog/')
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    published_at = models.DateTimeField(_("Published At"), null=True, blank=True)
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-published_at']

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.translations.model.objects.get(language_code='en', master_id=self.id).title)
        
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
            
        super().save(*args, **kwargs)