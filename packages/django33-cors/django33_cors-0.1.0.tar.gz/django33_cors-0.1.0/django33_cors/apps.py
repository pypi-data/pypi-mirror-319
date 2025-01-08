from __future__ import annotations

from django33.apps import AppConfig
from django33.core.checks import Tags
from django33.core.checks import register

from django33_cors.checks import check_settings


class CorsHeadersAppConfig(AppConfig):
    name = "django33_cors"
    verbose_name = "django-cors-headers"

    def ready(self) -> None:
        register(Tags.security)(check_settings)
