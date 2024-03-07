import json
from flask import Flask, request, render_template, redirect

app = Flask(__name__)


def get_commands_from_json(id: str) -> dict:
    try:
        with open(f"app/data/{id}.json", "r") as f:
            return json.load(f)
    except Exception:
        return {"commands": []}


@app.get("/")
def main_get():
    commands = get_commands_from_json("cmd_to_execute")
    commands = {"commands": []} if commands == {} else commands

    return render_template("main.html", commands=commands)


@app.post("/")
def main_post():
    cmd: str = request.form.get("cmd")
    commands = get_commands_from_json("cmd_to_execute")
    commands["commands"].append(cmd)
    with open(f"app/data/cmd_to_execute.json", "w+") as json_file:
        json.dump(obj=commands, fp=json_file, indent=4)

    return redirect("/", 201)


@app.get("/cmd1")
def usr():
    return "ls /usr"


@app.get("/cmd2")
def opt():
    return "ls /opt"


@app.post("/output")
def output_post():
    try:
        with open(f"output_history.json", "r") as json_file:
            output_history = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        output_history = {"history": []}

    data: dict = request.get_json()
    output_history["history"].append(data)

    with open(f"output_history.json", "w+") as json_file:
        json.dump(obj=output_history, fp=json_file, indent=4)

    return "OK", 201


@app.get("/output")
def output_get():
    try:
        with open(f"output_history.json", "r") as json_file:
            output_history = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        output_history: dict = {"history": []}

    return output_history


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
