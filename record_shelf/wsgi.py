"""WSGI config for the Record Shelf project."""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "record_shelf.settings")

application = get_wsgi_application()
