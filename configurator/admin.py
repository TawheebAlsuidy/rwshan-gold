from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from configurator.models.configurator_models import UniformDesign


@admin.register(UniformDesign)
class UniformDesignAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'fabric', 'color', 'created_at', 'get_total_price']
    list_filter = ['product', 'fabric', 'color', 'created_at']
    search_fields = ['user__username', 'user__email', 'notes']
    readonly_fields = ['created_at', 'updated_at', 'get_total_price']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price()} SAR"
    get_total_price.short_description = _('Total Price')