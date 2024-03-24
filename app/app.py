from os import listdir
from app_functions import (
    get_commands_from_json,
    dump_commands_to_json,
    get_current_timestamp,
    last_ping_time_ago,
)
from flask import Flask, request, render_template, redirect, url_for
import flask_login

app = Flask(__name__)
app.secret_key = "Super_secret_KEY!$%"
app.url_map.strict_slashes = False

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {"Lukasz": {"password": "xxx"}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email

    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return

    user = User()
    user.id = email

    return user


@app.get("/")
def home():
    ls = listdir("app/data")
    id_list = [x.split(".json")[0] for x in ls if ".json" in x and "_out" not in x]
    machines = dict()
    for id in id_list:
        commands = get_commands_from_json(id)
        machines[id] = last_ping_time_ago(commands["pings"][0])

    return render_template("home.html", machines=machines)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    if email in users and request.form["password"] == users[email]["password"]:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for("protected"))

    return "Bad login"


@app.route("/protected")
@flask_login.login_required
def protected():
    return "Logged in as: " + flask_login.current_user.id


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized", 401


@app.get("/<machine_id>")
def machine_get(machine_id):
    commands = get_commands_from_json(machine_id)
    last_ping = last_ping_time_ago(commands["pings"][0])
    history = get_commands_from_json(machine_id, history=True)

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
    if len(output_history["commands"]) >= 15:
        output_history["commands"].pop(-1)
    dump_commands_to_json(machine_id, output_history, history=True)

    return "OK", 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
