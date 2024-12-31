from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DISCORD_TOKEN: str
    TELEGRAM_TOKEN: str

    GUILDS_FILE: str = "guilds.json"
    PARTICIPANTS_FILE: str = "participants.json"

    SYNC_COMMANDS: bool = False


settings = Settings()
