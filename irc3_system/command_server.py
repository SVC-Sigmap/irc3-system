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
import irc3_system.data_collection as data_collection
import irc3_system.signal_scanner as signal_scanner
import irc3_system.hallway_travel as hallway_travel

server = Flask(__name__)

ros2_path = '/opt/ros/humble/bin/ros2'
processes = [] # Define an empty list for processes to be stored. This way we can terminate all running subprocesses later.

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
                        undock_action = subprocess.Popen([ros2_path, 'action', 'send_goal', '/undock', 'irobot_create_msgs/action/Undock', '{}'])
                        processes.append(undock_action)
                    except KeyboardInterrupt:
                        pass
                    print('Undock command executed')
                    
                    return "Undock Executed"
                
                case 'StopAll':
                    # Terminates all processes that have been appended to the processes list
                    print("StopAll Command Recieved\nTerminating all active subprocesses...")
                    
                    for p in processes:
                        p.terminate()
                        
                    for p in processes:
                        p.wait()
                        
                    print("All Robot commands terminated successfully")
                        
                    return "All processes terminated"
                
                case 'HallwayTravel':
                    try:
                        hallway_travel()
                    except KeyboardInterrupt:
                        pass
                    
                    return "Hallway travel complete"
                
                case _:
                    
                    return "Unknown Command"
                
        else:
            return "Webhook received without command!"

