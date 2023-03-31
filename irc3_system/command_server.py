#!/usr/bin/env python3
#-------------------------------------------------------------------
#  File: command_server.py
#  Summary: Flask server that will serve data out on an API and recieve robot
#           commands as webhooks
#  Functions:
#           authenticate_request()
#           returns error if something is wrong with auth, otherwise passes request to other funcs
#           get_signal()
#           returns jsonified signal info
#           get_status()
#           returns jsonified status info about the robot
#           webhook()
#           recieves robot commands via POST and performs the corresponding command
#-------------------------------------------------------------------
from flask import Flask, request, jsonify
from firebase_admin import auth, credentials
import subprocess, firebase_admin
import irc3_system.robot_status as robot_status
import irc3_system.signal_scanner as signal_scanner
from irc3_system.hallway_travel import hallway_travel

server = Flask(__name__) # Creates the Flask application with the never 'server'.

ros2_path = '/opt/ros/humble/bin/ros2' # Absolute path to where the ros2 binary is located so we don't have to rely on $PATH
processes = [] # Define an empty list for processes to be stored. This way we can terminate all running subprocesses later.

# Try to load credentials from /opt, this is the easiest to do when running via container.
# If creds are not found in /opt then just pull them from the same directory.
try:
    cred = credentials.Certificate('/opt/irc3-system/sigmap.firebase.json')
except:
    cred = credentials.Certificate('sigmap.firebase.json')
    
firebase_admin.initialize_app(cred) # Start firebase SDK with our credentials

#-------------------------------------------------------------------
#  Function: authenticate_request()
#  Summary: Using @server.before_request, we use this function to validate if incoming POST and GET requests
#           contain the firebase auth token. If a firebase auth token is present, validate the token
#           against our firebase SDK using the loaded credentials from earlier.
#  Params: None
#  Returns: JSONified error if invalid token or missing header, along with status code 401
#           Returns nothing if valid, but authenticates the reqest.
#-------------------------------------------------------------------
@server.before_request
def authenticate_request():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'authorization header missing'}), 401
    try:
        decoded_token = auth.verify_id_token(token)
        request.current_user = decoded_token
    except:
        return jsonify({'error': 'invalid token'}), 401

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
    signal_data = signal_scanner.get_signal_data()
    signal_data['current_user'] = request.current_user # appends current firebase authenticated user to the JSON
    return jsonify(signal_data)

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
    status_data = robot_status.robot_status
    status_data['current_user'] = request.current_user # appends current firebase authenticated user to the JSON
    return jsonify(status_data)

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
                
                case 'HallwayTravel':
                    try:
                        hallway_travel(processes)
                    except KeyboardInterrupt:
                        pass
                    
                    return "Hallway travel complete"
                
                case _:
                    
                    return "Unknown Command"
                
        else:
            return "Webhook received without command!"

