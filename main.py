#!/usr/bin/env python3
#-------------------------------------------------------------------
#  File: main.py
#  Summary: Main python executable that will call and run all parts of the
#           iRC3 system
#-------------------------------------------------------------------
import irc3_system.command_server as command_server

def main():
    command_server.server.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()