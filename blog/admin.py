from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from blog.models.blog_models import PostCategory, Post


@admin.register(PostCategory)
class PostCategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    search_fields = ['translations__name']
    # prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ['title', 'category', 'author', 'status', 'published_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['translations__title', 'translations__content']
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'published_at']

    def save_model(self, request, obj, form, change):
        if obj.status == 'published' and not obj.published_at:
            from django.utils import timezone
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)
