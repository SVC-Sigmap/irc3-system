#!/usr/bin/env python3
#-------------------------------------------------------------------
#  File: commmand_server/server.py
#  Summary: Python script that creates a HTTP server that listens for specific custom HTTP GET headers.
#           Translates these headers into ROS2 instructions and/or scripts to be run on the middle-man hardware.
#  Functions:
#  run_server(server_class, handler_class, port)
#-------------------------------------------------------------------
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, os

class Server(BaseHTTPRequestHandler):
    def _set_reponse(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        logging.info("GET Request,\nPath: %s\nHeaders:\n%s\n", str(self.path,), str(self.headers))
        
        # Robot Commands
        
        match self.headers.get('SIGMAP-CMD'):
            case 'Undock':
                print("Undock command received...")
                os.system(f'ros2 action send_goal /undock irobot_create_msgs/action/Undock "{{}}"')
                print("Undock completed.")
            case _:
                print("Unknown SIGMAP-CMD")

        self._set_reponse()

#-------------------------------------------------------------------
#  Function: run_server
#  Summary: Creates the HTTP server using the implementation class created above
#  Params: server_class
#          The server will be running as HTTPServer
#          handler_class
#          HTTPServer will run with handler implementation created above called Server
#          port
#          Sets port the server will run on
#  Returns: Description
#-------------------------------------------------------------------
def run_server(server_class=HTTPServer, handler_class=Server, port=8080):
    logging.basicConfig(level=logging.INFO)
    address = ('', port)
    http_daemon = server_class(address, handler_class)
    logging.info('Starting http daemon...\n')
    try:
        http_daemon.serve_forever()
    except KeyboardInterrupt:
        pass
    http_daemon.server_close()
    logging.info("Stopping http daemon")
    
run_server()