from app.core.config.base import AppSettings


class TestSettings(AppSettings):
    env: str = "testing"
    debug: bool = True

    # Overwrite default URLs to test isolations
    def model_post_init(self, __context) -> None:
        super().model_post_init(__context)
        if not self.db.url:
            self.db.url = "postgresql+asyncpg://postgres:postgrespassword@localhost:5432/sentinel_test"
        if not self.cache.url:
            self.cache.url = "redis://localhost:6379/1"
        if self.vector.url == "http://qdrant:6333":
            self.vector.url = "http://localhost:6333"
