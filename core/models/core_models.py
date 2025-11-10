from django.db import models
from django.utils.translation import gettext_lazy as _


class GeneralSetting(models.Model):
    key = models.CharField(_('Key'), max_length=100, unique=True)
    value = models.TextField(_('Value'))
    description = models.TextField(_('Description'), blank=True)
    
    class Meta:
        verbose_name = _('General Setting')
        verbose_name_plural = _('General Settings')
    
    def __str__(self):
        return self.key