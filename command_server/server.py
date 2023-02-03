#!/usr/bin/env python3

from flask import Flask, request, jsonify
import os

server = Flask(__name__)

# this is "fake" data for now to test connection between the server and the app. This should be replaced with
# functional checks at a later date
robot_status = [
    {'Battery': 99, 'Name': 'Wifibot-0', 'Ready': True, 'Scanning': False}
]

@server.route('/status')
def get_status():
    return jsonify(robot_status)

@server.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        content = request.get_json()
        print('Webhook JSON:')
        print(content)

        if content.get('SIGMAP-CMD'):
            print('SIGMAP-CMD Present in POST JSON')
            match content.get('SIGMAP-CMD'):
                case 'Undock':
                    print('Undock Command Recieved!')
                    os.system(f'ros2 action send_goal /undock irobot_create_msgs/action/Undock "{{}}"')
                    print('Undock command executed')
                case _:
                    print("Unknown Command")

        return "Webhook Recieved!"

server.run(host='0.0.0.0', port=8080)
