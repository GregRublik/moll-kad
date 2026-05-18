from pydantic_settings import BaseSettings, SettingsConfigDict

class KadSettings(BaseSettings):
    api_key: str

    model_config = SettingsConfigDict(
        env_prefix="KAD_", env_file=".env", extra="ignore"
    )

class BitrixSettings(BaseSettings):
    webhook_url: str
    url: str

    model_config = SettingsConfigDict(env_prefix="BITRIX_", env_file=".env", extra="ignore")


class Settings(BaseSettings):
    kad: KadSettings
    bitrix: BitrixSettings

settings = Settings(
    kad=KadSettings(),
    bitrix=BitrixSettings(),
)