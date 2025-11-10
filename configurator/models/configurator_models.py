from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from products.models.product_models import Product, FabricOption, ColorOption


class UniformDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    fabric = models.ForeignKey(FabricOption, on_delete=models.CASCADE, verbose_name=_("Fabric"))
    # color = models.ForeignKey(ColorOption, on_delete=models.CASCADE, verbose_name=_("Color"))
    color = models.CharField(
        max_length=7,  # لتخزين كود HEX مثل #FF0000
        verbose_name=_("Color"),
        default='#000000'
    )
    logo = models.ImageField(_("Logo"), upload_to='design_logos/', null=True, blank=True)
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    ai_preview = models.ImageField(_("AI Preview"), upload_to='design_previews/', null=True, blank=True)

    # logo_nobg = models.ImageField(upload_to='logos_nobg/', blank=True, null=True)
    # final_preview = models.ImageField(upload_to='final_previews/', blank=True, null=True)

    class Meta:
        verbose_name = _("Uniform Design")
        verbose_name_plural = _("Uniform Designs")

    def __str__(self):
        return f"{self.product.name} - {self.user.username if self.user else 'Anonymous'}"

    def get_total_price(self):
        base_price = self.product.base_price
        fabric_modifier = self.fabric.price_modifier
        return base_price + fabric_modifier