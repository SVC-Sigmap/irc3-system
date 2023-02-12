# iRobot Create 3 Backend for Sigmap

This repo contains the backend code for command, control, and data gathering on the iRobot Create 3 platform for the Sigmap project.

## Usage

This backend is intended to be run on a Pi 4 on-board the Create 3.

```shell
$ pip install -r requirements.txt
$ ./main.py
```

### Other Dependencies:
- `iwconfig`

## Testing

| Module | Unit Test | Passing |
| --- | --- | --- |
| [command_server](https://github.com/SVC-Sigmap/irc3-system/blob/main/irc3_system/command_server.py) | [test_command_server](https://github.com/SVC-Sigmap/irc3-system/blob/main/tests/test_command_server.py) | Yes |
| [signal_scanner](https://github.com/SVC-Sigmap/irc3-system/blob/main/irc3_system/signal_scanner.py) | [test_signal_scanner](https://github.com/SVC-Sigmap/irc3-system/blob/main/tests/test_signal_scanner.py) | Yes
| [data_collection](https://github.com/SVC-Sigmap/irc3-system/blob/main/irc3_system/data_collection.py) | None | N/A |
