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

import os
from typing import Text

from ament_index_python.packages import get_package_share_directory, PackageNotFoundError

from launch import LaunchContext, LaunchDescription, SomeSubstitutionsType, Substitution
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

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
                case 'Teleop_Keyboard':
                    
                    print('Teleop_Keyboard Command Recieved!')
                    try:
                        teleop_keyboard = subprocess.Popen([ros2_path, 'ros2', 'run', 'teleop_twist_keyboard', 'teleop_twist_keyboard','{}'])
                        processes.append(teleop_keyboard)
                    except KeyboardInterrupt:
                        pass
                    print('Telelop_Keyboard command executed')
                    
                    return "Teleop_Keyboard Action Executed"
                    
                case 'Teleoperation_Joystick':
                    
                    print('Teleop_Joystick Command Recieved!')
                    try:
                        teleop_joystick = subprocess.Popen([ros2_path, 'ros2', 'launch', 'create3_teleop', 'teleop_joystick_launch.py', 'joy_dev:=/dev/input/js1','{}'])
                        processes.append(teleop_joystick)
                    except KeyboardInterrupt:
                        pass
                    print('Teleop_Joystick command executed')
                    
                    return "Teleop_Joystick Action Executed"                    

                case 'StopAll':
                    # Terminates all processes that have been appended to the processes list
                    print("StopAll Command Recieved\nTerminating all active subprocesses...")
                    
                    for p in processes:
                        p.terminate()
                        
                    for p in processes:
                        p.wait()
                        
                    print("All Robot commands terminated successfully")
                        
                    return "All processes terminated"
                
                case _:
                    
                    return "Unknown Command"
                
        else:
            return "Webhook received without command!"

