import json


def get_commands_from_json(id: str, history: bool=False) -> dict:
    json_path = f"app/data/{id}_out.json" if history else f"app/data/{id}.json"
    try:
        with open(json_path, "r") as json_file:
            return json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"commands": []}


def dump_commands_to_json(id: str, commands: dict, history: bool=False) -> None:
    json_path = f"app/data/{id}_out.json" if history else f"app/data/{id}.json"
    with open(json_path, "w+") as json_file:
        json.dump(obj=commands, fp=json_file, indent=4)
