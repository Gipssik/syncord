import json
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_map_from_json(filename: str) -> dict[int, Union[int, str]]:
    with open(filename, "r") as file:
        data = file.read()
    dict_data = json.loads(data)
    return {int(key): value for key, value in dict_data.items()}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    GUILDS_MAP: dict[int, int] = get_map_from_json("guilds.json")
    PARTICIPANTS_MAP: dict[int, str] = get_map_from_json("participants.json")

    DISCORD_TOKEN: str
    TELEGRAM_TOKEN: str

    SYNC_COMMANDS: bool = False


settings = Settings()
