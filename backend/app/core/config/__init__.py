import os
from app.core.config.base import AppSettings
from app.core.config.dev import DevSettings
from app.core.config.prod import ProdSettings
from app.core.config.test import TestSettings

# Read configuration profile from environment variable APP_ENV or fallback to ENV
app_env = os.getenv("APP_ENV", os.getenv("ENV", "development")).lower()

if app_env == "production":
    settings: AppSettings = ProdSettings()
elif app_env == "testing":
    settings = TestSettings()
else:
    settings = DevSettings()

# Export settings
__all__ = ["settings", "AppSettings"]
