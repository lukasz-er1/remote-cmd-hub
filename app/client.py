import requests
import argparse
from uuid import uuid4
from subprocess import getoutput
from dotenv import dotenv_values, set_key
from time import sleep
from datetime import datetime


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

    parser = argparse.ArgumentParser()
    parser.add_argument("--api_url", help="Server URL")
    parser.add_argument("--user_id", help="User ID on the server side")

    args, _ = parser.parse_known_args()
    config = dotenv_values(".env")

    if args.api_url:
        api_url = args.api_url
        set_key(".env", "api_url", api_url)
    else:
        api_url = config.get("api_url")
        if api_url is None:
            api_url = input(f"Enter server URL: ")
            set_key(".env", "user_id", api_url.strip())
        else:
            print(f"Client will use server URL from env: {api_url}.")

    if args.user_id:
        user_id = args.user_id
        set_key(".env", "user_id", user_id)
    else:
        user_id = config.get("user_id")
        if user_id is None:
            user_id = input(f"Enter your user ID from {api_url}: ")
            if len(user_id) == 36:
                set_key(".env", "user_id", user_id.strip())
            else:
                raise ValueError(f"Provided user ID ({user_id}) is invalid (it needs to be 36 characters long)")

    machinde_id = config.get("machinde_id")
    if machinde_id is None:
        machinde_id = str(uuid4())
        set_key(".env", "machinde_id", machinde_id)

    while True:
        execute_cmd_from_server(machinde_id)
        sleep(10)
