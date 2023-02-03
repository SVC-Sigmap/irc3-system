#!/usr/bin/env python3

from flask import Flask, request, jsonify
import os
import data_collection

server = Flask(__name__)


@server.route('/status')
def get_status():
    return jsonify(data_collection.robot_status)

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

