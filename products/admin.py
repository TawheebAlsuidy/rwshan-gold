from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from products.models.product_models import ProductCategory, Product, FabricOption, ColorOption
from parler.admin import TranslatableAdmin


@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'description', 'icon')
    def name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    # def product_count(self, obj):
    #     return obj.products.count()
    # product_count.short_description = _('Product Count')

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('name', 'description', 'category', 'base_price', 'image_preview','fabric','color')

    def name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return _("No Image")
    image_preview.short_description = _('Image Preview')
    
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name_ar', 'name_en', 'category', 'base_price', 'image_preview']
#     list_filter = ['category']
#     search_fields = ['name_ar', 'name_en']
    # prepopulated_fields = {'slug': ('name_en',)}
    
    


@admin.register(FabricOption)
class FabricOptionAdmin(TranslatableAdmin):
    list_display = ('name', 'price_modifier')

    def name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)



@admin.register(ColorOption)
class ColorOptionAdmin(TranslatableAdmin):
    list_display = ('name', 'hex_code')

    def name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    
    def color_display(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background-color: {}; border: 1px solid #ccc;"></span> {}',
            obj.hex_code, obj.hex_code
        )
    color_display.short_description = _('Color')