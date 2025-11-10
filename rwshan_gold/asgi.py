"""
ASGI config for rwshan_gold project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'rwshan_gold.settings.development' 
)

application = get_asgi_application()
