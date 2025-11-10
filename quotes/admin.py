from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from quotes.models.quote_models import QuoteRequest


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'contact_person', 'email', 'product', 'quantity', 'status', 'estimated_price', 'created_at']
    list_filter = ['status', 'product', 'created_at']
    search_fields = ['company_name', 'contact_person', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'estimated_price']
    
    actions = ['mark_as_contacted', 'mark_as_quoted', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')
    mark_as_contacted.short_description = _('Mark selected as contacted')
    
    def mark_as_quoted(self, request, queryset):
        queryset.update(status='quoted')
    mark_as_quoted.short_description = _('Mark selected as quoted')
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = _('Mark selected as completed')
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = _('Mark selected as cancelled')