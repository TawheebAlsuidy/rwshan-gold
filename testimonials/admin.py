# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
# from testimonials.models.testimonial_models import Testimonial, ClientPartner, CaseStudy


# @admin.register(Testimonial)
# class TestimonialAdmin(admin.ModelAdmin):
#     list_display = ['client_name', 'company', 'is_featured', 'created_at']
#     list_filter = ['is_featured', 'created_at']
#     search_fields = ['client_name_ar', 'client_name_en', 'company_ar', 'company_en']


# @admin.register(ClientPartner)
# class ClientPartnerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'website_url', 'is_featured', 'created_at']
#     list_filter = ['is_featured', 'created_at']
#     search_fields = ['name_ar', 'name_en']


# @admin.register(CaseStudy)
# class CaseStudyAdmin(admin.ModelAdmin):
#     list_display = ['title', 'client', 'created_at']
#     list_filter = ['client', 'created_at']
#     search_fields = ['title_ar', 'title_en']
#     prepopulated_fields = {'slug': ('title_en',)}

from django.contrib import admin
from parler.admin import TranslatableAdmin
from testimonials.models.testimonial_models import Testimonial, ClientPartner, CaseStudy, Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    search_fields = ['name']

@admin.register(Testimonial)
class TestimonialAdmin(TranslatableAdmin):
    list_display = ['client_name_en', 'company_en', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['client_name_en', 'client_name_ar', 'company_en', 'company_ar']

@admin.register(ClientPartner)
class ClientPartnerAdmin(TranslatableAdmin):
    list_display = ['name_en', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name_en', 'name_ar']

@admin.register(CaseStudy)
class CaseStudyAdmin(TranslatableAdmin):
    list_display = ['title_en', 'client', 'created_at']
    list_filter = ['client', 'created_at']
    search_fields = ['title_en', 'title_ar']
    prepopulated_fields = {'slug': ('title_en',)}