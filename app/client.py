import requests
import subprocess
from time import sleep
from datetime import datetime


api_url = "http://127.0.0.1:5000"


def execute_cmd_from_subpage(subpage: str) -> None:
    cmd = requests.get(f"{api_url}/{subpage}")
    curr_time = datetime.now().strftime("%H:%M:%S")
    output = subprocess.getoutput(cmd.text)
    data: dict = {"time": curr_time, "cmd": cmd.text, "output": output}
    requests.post(f"{api_url}/output", json=data)


if __name__ == "__main__":
    execute_cmd_from_subpage("cmd1")
    sleep(2)
    execute_cmd_from_subpage("cmd2")
