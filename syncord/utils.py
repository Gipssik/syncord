import json
from typing import Union


def get_map_from_json(filename: str) -> dict[int, Union[int, str]]:
    with open(filename, "r") as file:
        data = file.read()
    dict_data = json.loads(data)
    return {int(key): value for key, value in dict_data.items()}


def write_json_to_file(filename: str, data: dict[int, Union[int, str]]):
    with open(filename, "w") as file:
        json.dump(data, file)
