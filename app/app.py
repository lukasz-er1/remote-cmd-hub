import json
from flask import Flask, request, render_template

app = Flask(__name__)


@app.get("/")
def main_get():
    try:
        with open(f"cmd_to_execute.json", "r") as json_file:
            commands: dict = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        commands: dict = {"commands": []}

    return render_template("main.html", commands=commands)


@app.post("/")
def main_post():
    cmd = request.form.get("cmd")
    try:
        with open(f"cmd_to_execute.json", "r") as json_file:
            commands: dict = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        commands: dict = {"commands": []}
    commands["commands"].append(cmd)
    with open(f"cmd_to_execute.json", "w+") as json_file:
        json.dump(obj=commands, fp=json_file, indent=4)
    return cmd


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
            output_history: dict = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        output_history: dict = {"history": []}

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
