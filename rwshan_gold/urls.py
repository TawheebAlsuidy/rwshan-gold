"""
URL configuration for rwshan_gold project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
# import debug_toolbar

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

# Include app URLs with i18n patterns
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('configurator/', include('configurator.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('quotes/', include('quotes.urls')),
    path('blog/', include('blog.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('contact/', include('contact.urls')),
    prefix_default_language=False,
)

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]