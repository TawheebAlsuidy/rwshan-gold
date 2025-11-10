from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from contact.models.contact_models import ContactMessage, FAQ


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = _('Mark selected as read')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question_ar', 'question_en', 'answer_ar', 'answer_en']