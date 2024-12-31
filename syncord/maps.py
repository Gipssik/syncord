from syncord.config import settings
from syncord.utils import get_map_from_json

GUILDS_MAP: dict[int, int] = get_map_from_json(settings.GUILDS_FILE)
PARTICIPANTS_MAP: dict[int, str] = get_map_from_json(settings.PARTICIPANTS_FILE)
