"""ASGI config for the local lead generation project."""

from __future__ import annotations

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leadgen_site.settings")

application = get_asgi_application()
