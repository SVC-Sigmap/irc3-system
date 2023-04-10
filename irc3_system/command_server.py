#!/usr/bin/env python3
#-------------------------------------------------------------------
#  File: command_server.py
#  Summary: Flask server that will serve data out on an API and recieve robot
#           commands as webhooks
#  Functions:
#           get_signal()
#           returns jsonified signal info
#           get_status()
#           returns jsonified status info about the robot
#           webhook()
#           recieves robot commands via POST and performs the corresponding command
#-------------------------------------------------------------------
from flask import Flask, request, jsonify
import subprocess
import irc3_system.data_collection as data_collection
import irc3_system.signal_scanner as signal_scanner

server = Flask(__name__) # Creates the Flask application with the never 'server'.

ros2_path = '/opt/ros/humble/bin/ros2' # Absolute path to where the ros2 binary is located so we don't have to rely on $PATH
processes = [] # Define an empty list for processes to be stored. This way we can terminate all running subprocesses later.

#-------------------------------------------------------------------
#  Function: get_signal()
#  Summary: Every time a request is made to the /api/signal endpoint, we run 
#           the get_signal_data() function from the signal_scanner module.
#           This endpoint will give us various data about the signal strength.
#  Endpoint: /api/signal
#  Params: None
#  Returns: JSONified signal data.
#-------------------------------------------------------------------
@server.route('/api/signal')
def get_signal():
    return jsonify(signal_scanner.get_signal_data())

#-------------------------------------------------------------------
#  Function: get_status()
#  Summary: Gives a JSON for status information about the robot.
#           Data comes from seperate module function.
#  Endpoint: /api/status
#  Params: None
#  Returns: JSONified status data.
#-------------------------------------------------------------------
@server.route('/api/status')
def get_status():
    return jsonify(data_collection.robot_status)

#-------------------------------------------------------------------
#  Function: webhook()
#  Summary: Takes in POST requests and checks the JSON body for valid commands
#           that will be translated into ROS2 robot commands.
#  Endpoint: /webhooks/cmd
#  Params: None
#  Returns: Status message and status code
#-------------------------------------------------------------------
@server.route('/webhooks/cmd', methods=['POST'])
def webhook():
    if request.method == 'POST': # First checks to make sure the request is a POST method, otherwise it immediately returns
        content = request.get_json()
        print('Webhook JSON:') # Print JSON server-side
        print(content)

        if content.get('SIGMAP-CMD'): # Checking for SIGMAP-CMD key in the JSON body. This is the key we store out command in.
            print('SIGMAP-CMD Present in POST JSON')
            match content.get('SIGMAP-CMD'):
                case 'Teleop_Keyboard':
                    
                    print('Teleop_Keyboard Command Recieved!')
                    try:
                        # Start a subprocess to start teleop
                        teleop_keyboard = subprocess.Popen([ros2_path, 'run', 'teleop_twist_keyboard', 'teleop_twist_keyboard'])
                        processes.append(teleop_keyboard)
                    except KeyboardInterrupt:
                        pass
                    print('Teleop_Keyboard command executed')
                    
                    return "Teleop_Keyboard Action Executed"
                    
                case 'Teleoperation_Joystick':
                    
                    print('Teleop_Joystick Command Recieved!')
                    try:
                        teleop_joystick = subprocess.Popen([ros2_path, 'launch', 'create3_teleop', 'teleop_joystick_launch.py', 'joy_dev:=/dev/input/js0'])
                        processes.append(teleop_joystick)
                    except KeyboardInterrupt:
                        pass
                    print('Teleop_Joystick command executed')
                    
                    return "Teleop_Joystick Action Executed"                    

                case 'StopAll':
                    # Terminates all processes that have been appended to the processes list
                    print("StopAll Command Recieved\nTerminating all active subprocesses...")
                    
                    for p in processes:
                        p.kill()
                        
                    for p in processes:
                        p.wait()
                        
                    print("All Robot commands terminated successfully")
                        
                    return "All processes terminated"
                
                case _:
                    
                    return "Unknown Command"
                
        else:
            return "Webhook received without command!"

