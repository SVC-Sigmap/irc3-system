#!/usr/bin/env python3
#-------------------------------------------------------------------
#  File: command_server.py
#  Summary: Flask server that will serve data out on an API and recieve robot
#           commands as webhooks
#  Functions:
#           get_status()
#           returns jsonified status info about the robot
#           webhook()
#           recieves robot commands via POST and performs the corresponding command
#-------------------------------------------------------------------
from flask import Flask, request, jsonify
import subprocess
import data_collection
import signal_scanner

server = Flask(__name__)

ros2_path = '/opt/ros/humble/bin/ros2'

@server.route('/api/signal')
def get_signal():
    return jsonify(signal_scanner.get_signal_data())

@server.route('/api/status')
def get_status():
    return jsonify(data_collection.robot_status)

@server.route('/webhooks/cmd', methods=['POST'])
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
                    try:
                        undock_action = subprocess.run([ros2_path, 'action', 'send_goal', '/undock', 'irobot_create_msgs/action/Undock', '{}'])
                    except KeyboardInterrupt:
                        pass
                    print('Undock command executed')
                    return "Undock Executed"
                case _:
                    return "Unknown Command"
        else:
            return "Webhook received without command!"

