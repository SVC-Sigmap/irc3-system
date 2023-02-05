# iRobot Create 3 Backend for Sigmap

This repo contains the backend code for command, control, and data gathering on the iRobot Create 3 platform for the Sigmap project.

## Usage

This backend is intended to be run on a Pi 4 on-board the Create 3.

```shell
$ pip install -r requirements.txt
$ ./main.py
```

## Testing
[command_server_test.py](https://github.com/SVC-Sigmap/irc3-system/blob/main/command_server_test.py)
```stdout
$ python3 -m unittest command_server_test.py 
.Webhook JSON:
{'SIGMAP-CMD': 'Undock'}
SIGMAP-CMD Present in POST JSON
Undock Command Recieved!
Waiting for an action server to become available...
Sending goal:
     {}

Goal accepted with ID: 2b64f1b04ae44786ac0aabb359110509

Result:
    is_docked: false

Goal finished with status: SUCCEEDED
Undock command executed
Webhook JSON:
{'SIGMAP-CMD': 'Invalid'}
SIGMAP-CMD Present in POST JSON
Webhook JSON:
{}
.
----------------------------------------------------------------------
Ran 2 tests in 7.969s

OK
```
