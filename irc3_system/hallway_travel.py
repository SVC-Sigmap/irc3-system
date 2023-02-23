import subprocess
from math import pi
pos_turn = pi / 2
neg_turn = pi / 2

def hallway_travel(processes):
    max_zigzag = 4
    ros2_path = "/opt/ros/humble/bin/ros2"
    undock_action = subprocess.Popen([ros2_path, 'action', 'send_goal', '/undock', 'irobot_create_msgs/action/Undock', '{}'])
    processes.append(undock_action)

    for p in processes:
        p.wait()
    #undock_action.wait()
    #undock_action.kill()

    for i in range(max_zigzag):
        forward = subprocess.Popen([ros2_path, 'action', 'send_goal', '/drive_distance', 'irobot_create_msgs/action/DriveDistance', '{distance: 1.8,max_translation_speed: 0.5}'])
        processes.append(forward)

        for p in processes:
            p.wait()
            p.kill()

        #forward.wait()
        #forward.kill()
        
        #rotate_clockwise = subprocess.Popen([ros2_path, 'action', 'send_goal', '/rotate_angle', 'irobot_create_msgs/action/RotateAngle', '{angle: 1.57,max_rotation_speed: 0.75}'])
        rotate_clockwise = subprocess.Popen([ros2_path, 'action', 'send_goal', '/rotate_angle', 'irobot_create_msgs/action/RotateAngle', '{angle: ' + str(pos_turn) + ',max_rotation_speed: 0.75}'])
        processes.append(rotate_clockwise)

        for p in processes:
            p.wait()
            p.kill()
            
        #rotate_clockwise.wait()
        #rotate_clockwise.kill()
            
        forward = subprocess.Popen([ros2_path, 'action', 'send_goal', '/drive_distance', 'irobot_create_msgs/action/DriveDistance', '{distance: 1.8,max_translation_speed: 0.5}'])
        processes.append(forward)

        for p in processes:
            p.wait()
            p.kill()

        #forward.wait()
        #forward.kill()

        #rotate_counterclockwise = subprocess.Popen([ros2_path, 'action', 'send_goal', '/rotate_angle', 'irobot_create_msgs/action/RotateAngle', '{angle: -1.57,max_rotation_speed: 0.75}'])
        rotate_counterclockwise =  subprocess.Popen([ros2_path, 'action', 'send_goal', '/rotate_angle', 'irobot_create_msgs/action/RotateAngle', '{angle: ' + '-' + str(neg_turn) + ',max_rotation_speed: 0.75}'])
        processes.append(rotate_counterclockwise)

        for p in processes:
            p.wait()
            p.kill()
        
        #rotate_counterclockwise.wait()
        #rotate_counterclockwise.kill()

    print("Done Traveling Hallway!")
    
