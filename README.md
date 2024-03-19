# remote-cmd-hub
This web application, built using Flask in Python, is designed to execute commands on remote computers without using SSH, Telnet, VNC, etc.

Access in one way - from the client to the server is the only requirement. Remote machine can be also behind VPN, because the communication is ongoing only in one side: client --> server.

Command execution occurs by having the remote computers query the server for pending commands to execute. 

If commands are available, the remote computer executes them and returns the output using the POST request to the server API.


## Features
- Execute commands on remote computers via a web interface.

- View command execution output history in the web application interface.

- Choose machine for sending command.

- Queue commands.


## To do:
- User login

- Database instead of json files


## Installation
Clone the repository:
```bash
git clone https://github.com/lukasz-er1/remote-cmd-hub.git
```

Install dependencies:
```bash
cd remote-cmd-hub
pip install -r requirements_server.txt
```

Run the server:
```bash
python app/app.py
```

Run the client:
```bash
pip install -r requirements_client.txt
python app/client.py
```

Access the web interface of the application using a web browser on http://127.0.0.1:5000.

Enter the command you want to execute on a remote client.

Wait for the remote computer to query the server and execute the command.

View the output of the command execution in the web interface.
