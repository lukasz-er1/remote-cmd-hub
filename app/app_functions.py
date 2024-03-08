import json


def get_commands_from_json(id: str) -> dict:
    try:
        with open(f"app/data/{id}.json", "r") as f:
            return json.load(f)
    except Exception:
        return {"commands": []}


def dump_commands_to_json(id: str, commands: dict) -> None:
    with open(f"app/data/{id}.json", "w+") as json_file:
        json.dump(obj=commands, fp=json_file, indent=4)
