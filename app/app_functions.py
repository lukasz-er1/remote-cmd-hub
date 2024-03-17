import json
from time import time


def get_commands_from_json(id: str, history: bool = False) -> dict:
    json_path = f"app/data/{id}_out.json" if history else f"app/data/{id}.json"
    try:
        with open(json_path, "r") as json_file:
            return json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"commands": [], "pings": [0]}


def dump_commands_to_json(id: str, commands: dict, history: bool = False) -> None:
    json_path = f"app/data/{id}_out.json" if history else f"app/data/{id}.json"
    with open(json_path, "w+") as json_file:
        json.dump(obj=commands, fp=json_file, indent=4)


def get_current_timestamp() -> int:
    return int(time())


def last_ping_time_ago(last_ping: int) -> str:
    curr_time = int(time())
    difference = curr_time - last_ping
    if difference == 1:
        return "1 second ago"
    elif difference < 120:
        return f"{difference} seconds ago"
    elif 120 <= difference < 7200:
        return f"{int(difference / 60)} minutes ago"
    else:
        return f"{int(difference / 3600)} hours ago"
