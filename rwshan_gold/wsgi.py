"""
WSGI config for rwshan_gold project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'rwshan_gold.settings.development'
)

application = get_wsgi_application()
