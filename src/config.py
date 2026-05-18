from pydantic_settings import BaseSettings, SettingsConfigDict

class KadSettings(BaseSettings):
    api_key: str

    model_config = SettingsConfigDict(
        env_prefix="KAD_", env_file=".env", extra="ignore"
    )

class Settings(BaseSettings):
    kad: KadSettings

settings = Settings(
    kad=KadSettings(),
)