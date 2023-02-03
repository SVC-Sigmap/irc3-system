#!/usr/bin/env python3
import command_server

def main():
    command_server.server.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()