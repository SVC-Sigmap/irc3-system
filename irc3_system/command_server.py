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
                case 'Teleoperation':
                    
                    print('Teleoperation Command Recieved!')
                    try:
                        undock_action = subprocess.Popen([ros2_path, 'action', 'send_goal', '/undock', 'irobot_create_msgs/action/Undock', '{}'])
                        processes.append(undock_action)
                    except KeyboardInterrupt:
                        pass
                    print('Undock command executed')
                    
                    return "Undock Executed"

                    class JoystickConfigParser(Substitution):
                         def __init__(
                            self,
                            package_name: Text,
                            device_type: SomeSubstitutionsType
                         ) -> None:
                            self.__package_name = package_name
                            self.__device_type = device_type
                         def perform(
                                self,
                                context: LaunchContext = None,
                         ) -> Text:
                                device_type_str = self.__device_type.perform(context)
                                package_str = self.__package_name
                                try:
                                    package_share_dir = get_package_share_directory(
                                        package_str)
                                    config_filepath = [package_share_dir, 'config',
                                                     f'{device_type_str}.config.yaml']
                                    return os.path.join(*config_filepath)
                                except PackageNotFoundError:
                                    raise PackageNotFoundError(package_str)
                         def generate_launch_description():
                             joy_config = LaunchConfiguration('joy_config')
                             joy_dev = LaunchConfiguration('joy_dev')

                             # Invokes a node that interfaces a generic joystick to ROS 2.
                             joy_node = Node(package='joy', executable='joy_node', name='joy_node',
                                            parameters=[{
                                                'dev': joy_dev,
                                                'deadzone': 0.3,
                                                'autorepeat_rate': 20.0,
                                            }])

                             # Retrieve the path to the correct configuration .yaml depending on
                             # the joy_config argument
                             config_filepath = JoystickConfigParser('teleop_twist_joy', joy_config)

                             # Publish unstamped Twist message from an attached USB Joystick.
                             teleop_node = Node(package='teleop_twist_joy', executable='teleop_node',
                                                name='teleop_twist_joy_node', parameters=[config_filepath])
                             # Declare launchfile arguments
                             ld_args = []
                             ld_args.append(DeclareLaunchArgument('joy_config',
                                                                 default_value='xbox',
                                                                 choices=['xbox', 'ps3', 'ps3-holonomic', 'atk3', 'xd3']))
                             ld_args.append(DeclareLaunchArgument('joy_dev',
                                                                 default_value='/dev/input/js0'))
                             # Define LaunchDescription variable
                             ld = LaunchDescription(ld_args)

                             # Add nodes to LaunchDescription
                             ld.add_action(joy_node)
                             ld.add_action(teleop_node)

                             return ld

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

