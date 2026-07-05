from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    url: Optional[str] = None
    pool_size: int = 20
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 1800


class CacheSettings(BaseModel):
    url: Optional[str] = None
    timeout: float = 2.0


class VectorSettings(BaseModel):
    url: str = "http://qdrant:6333"
    api_key: Optional[str] = None


class LLMSettings(BaseModel):
    api_base: str = "http://ollama:11434"
    primary_model: str = "gemma2:9b"
    secondary_model: str = "qwen2.5-coder:7b"
    embedding_model: str = "nomic-embed-text"


class StorageSettings(BaseModel):
    endpoint: str = "minio:9000"
    access_key: str = "miniouser"
    secret_key: str = "miniopassword"
    secure: bool = False
    bucket_incidents: str = "sentinel-incidents"


class TelemetrySettings(BaseModel):
    enabled: bool = False
    otlp_endpoint: str = "http://otel-collector:4317"
    service_name: str = "sentinel-ai-backend"


class SecuritySettings(BaseModel):
    secret_key: str = "dev_secret_key_change_me_in_production_32_bytes_long"
    token_expiry_minutes: int = 60


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    env: str = "development"
    debug: bool = True
    project_name: str = "Sentinel AI"
    api_v1_str: str = "/api/v1"

    # Composability structure
    db: DatabaseSettings = DatabaseSettings()
    cache: CacheSettings = CacheSettings()
    vector: VectorSettings = VectorSettings()
    llm: LLMSettings = LLMSettings()
    storage: StorageSettings = StorageSettings()
    telemetry: TelemetrySettings = TelemetrySettings()
    security: SecuritySettings = SecuritySettings()
