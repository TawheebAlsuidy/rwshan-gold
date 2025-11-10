from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class ProductCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("Name"), max_length=100),
        description = models.TextField(_("Description"), blank=True),
    )
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    icon = models.ImageField(_("Icon"), upload_to='category_icons/')
    
    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

class FabricOption(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("Name"), max_length=100),
    )
    price_modifier = models.DecimalField(_("Price Modifier"), max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _("Fabric Option")
        verbose_name_plural = _("Fabric Options")
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class ColorOption(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("Name"), max_length=100),
    )
    hex_code = models.CharField(_("Hex Code"), max_length=7)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or self.hex_code
    
    class Meta:
        verbose_name = _("Color Option")
        verbose_name_plural = _("Color Options")
    


class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("Name"), max_length=100),
        description = models.TextField(_("Description"), blank=True),
    )
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    base_price = models.DecimalField(_("Base Price"), max_digits=10, decimal_places=2)
    image = models.ImageField(_("Image"), upload_to='products/')
    fabric = models.ForeignKey(FabricOption, on_delete=models.PROTECT, null=True, blank=True)
    color = models.ForeignKey(ColorOption, on_delete=models.PROTECT, null=True, blank=True)
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


