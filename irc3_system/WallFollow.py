import subprocess        
        
def wallFollow(process):
        

    ros2_path = "/opt/ros/humble/bin/ros2"
    undock_action = subprocess.Popen([ros2_path, 'action', 'send_goal', '/undock', 'irobot_create_msgs/action/Undock', '{}'])
    processes.append(undock_action)

    for p in processes:
        p.wait()


        wallFollow = subprocess.Popen([ros2_path, 'action', 'send_goal', '/wall_fallow', 'irobot_create_msgs/action/WallFollow', '{follow_side: 1, max_runtime: {sec: 5, nanosec: 0}}'])
        process.append(wallFollow)

        for p in processes:
            p.wait()
            p.kill()

        wallFollow = subprocess.Popen([ros2_path, 'action', 'send_goal', '/wall_fallow', 'irobot_create_msgs/action/WallFollow', '{follow_side: 1, max_runtime: {sec: 5, nanosec: 0}}'])
        process.append(wallFollow)

        for p in processes:
            p.wait()
            p.kill()

        wallFollow = subprocess.Popen([ros2_path, 'action', 'send_goal', '/wall_fallow', 'irobot_create_msgs/action/WallFollow', '{follow_side: 1, max_runtime: {sec: 5, nanosec: 0}}'])
        process.append(wallFollow)

        for p in processes:
            p.wait()
            p.kill()


