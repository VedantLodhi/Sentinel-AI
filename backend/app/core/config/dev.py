from app.core.config.base import AppSettings


class DevSettings(AppSettings):
    env: str = "development"
    debug: bool = True
