"""ASGI config for the Record Shelf project."""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "record_shelf.settings")

application = get_asgi_application()
