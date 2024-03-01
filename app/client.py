import requests
import subprocess

api_url = "http://127.0.0.1:5000"


if __name__ == "__main__":
    cmd = requests.get(api_url)
    output = subprocess.getoutput(cmd.text)

    data = {"cmd": cmd.text, "output": output}
    print(data)
