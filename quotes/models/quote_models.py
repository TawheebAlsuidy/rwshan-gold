from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from products.models.product_models import Product, FabricOption, ColorOption
from django.conf import settings
import uuid


class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', _('في الانتظار')),
        ('contacted', _('تم الاتصال')),
        ('quoted', _('مقتبس')),
        ('completed', _('اكتمل')),
        ('cancelled', _('ملغي')),
    ]
    
    LOGO_COMPLEXITY_CHOICES = [
        ('simple', _('بسيط')),
        ('medium', _('متوسط')),
        ('complex', _('معقد')),
    ]
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    fabric = models.ForeignKey(FabricOption, on_delete=models.CASCADE, verbose_name=_("Fabric"))
    color = models.ForeignKey(ColorOption, on_delete=models.CASCADE, verbose_name=_("Color"))
    quantity = models.PositiveIntegerField(_("Quantity"))
    logo_complexity = models.CharField(_("Logo Complexity"), max_length=20, choices=LOGO_COMPLEXITY_CHOICES)
    company_name = models.CharField(_("Company Name"), max_length=100)
    contact_person = models.CharField(_("Contact Person"), max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20)
    notes = models.TextField(_("Notes"), blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_price = models.DecimalField(_("Estimated Price"), max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    quote_id = models.CharField(max_length=20, unique=True, blank=True)
    class Meta:
        verbose_name = _("Quote Request")
        verbose_name_plural = _("Quote Requests")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} | {self.quote_id} - {self.product.name}"
    
    def save(self, *args, **kwargs):
        if not self.quote_id:
            self.quote_id = f"QR{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def calculate_price(self):
        base_price = self.product.base_price
        fabric_modifier = self.fabric.price_modifier
        quantity_discount = self.get_quantity_discount()
        logo_complexity_fee = self.get_logo_complexity_fee()
        
        unit_price = base_price + fabric_modifier + logo_complexity_fee
        total_price = unit_price * self.quantity * (1 - quantity_discount)
        
        self.estimated_price = total_price
        self.save()
        return total_price

    def get_quantity_discount(self):
        if self.quantity >= 100:
            return 0.15  # 15% discount
        elif self.quantity >= 50:
            return 0.10  # 10% discount
        elif self.quantity >= 20:
            return 0.05  # 5% discount
        return 0

    def get_logo_complexity_fee(self):
        fees = {
            'simple': 10,
            'medium': 25,
            'complex': 50
        }
        return fees.get(self.logo_complexity, 0)