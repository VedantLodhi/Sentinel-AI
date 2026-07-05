from pydantic import model_validator
from app.core.config.base import AppSettings


class ProdSettings(AppSettings):
    env: str = "production"
    debug: bool = False

    @model_validator(mode="after")
    def validate_prod_secrets(self) -> "ProdSettings":
        """Assert that security keys are not using development defaults in production."""
        if (
            self.security.secret_key
            == "dev_secret_key_change_me_in_production_32_bytes_long"
        ):
            raise ValueError(
                "SECRET_KEY must be changed from development default in production."
            )
        if not self.db.url:
            raise ValueError("Database URL (db.url) must be configured in production.")
        if not self.cache.url:
            raise ValueError("Redis URL (cache.url) must be configured in production.")
        return self
