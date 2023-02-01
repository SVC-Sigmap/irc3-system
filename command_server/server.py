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