from django.contrib import admin
from core.models.core_models import GeneralSetting


@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'description']
    search_fields = ['key', 'description']
    list_filter = ['key']
    
    def has_add_permission(self, request):
        # Restrict to only one instance per key
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False