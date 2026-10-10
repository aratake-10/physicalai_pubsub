#!/usr/bin/env python3

"""
Robot Action Publisher Module

Publishes joint trajectory commands to control the robot's movement via
'/crane_plus_arm_controller/joint_trajectory' topic.

Example:
    ros2 run physicalai_pubsub action_publisher
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

class RobotActionPublisher(Node):
    """
    ROS2 node that publishes joint trajectory commands for robot control.
    """

    def __init__(self):
        """Initialize publisher for joint trajectory commands."""
        super().__init__('robot_action_publisher')
        self.publisher = self.create_publisher(
            JointTrajectory,
            'crane_plus_arm_controller/joint_trajectory',
            10)
        self.get_logger().info('Robot Action Publisher node has been started')

    def move_to_position(self, positions, time_from_start=2.0):
        """
        Move robot joints to specified positions.

        Args:
            positions: List of joint positions in radians [joint1, joint2, joint3, joint4]
            time_from_start: Time to reach positions in seconds (default: 2.0)
        """
        msg = JointTrajectory()
        msg.joint_names = [
            'crane_plus_joint1',
            'crane_plus_joint2',
            'crane_plus_joint3',
            'crane_plus_joint4'
        ]

        point = JointTrajectoryPoint()
        point.positions = positions
        point.velocities = [0.0] * len(positions)
        point.accelerations = [0.0] * len(positions)
        point.time_from_start = Duration(sec=int(time_from_start), nanosec=int((time_from_start % 1) * 1e9))
        
        msg.points.append(point)
        self.publisher.publish(msg)
        self.get_logger().info(f'Published trajectory command: {positions}')

def main():
    rclpy.init()
    robot_action_publisher = RobotActionPublisher()

    try:
        # [j1(turn around), j2(shoulder), j3(elbow), j4(wrist)] rad
        waypoints = [
            ([0.0, 0.0, 0.0, 0.0], "home posture"),
            ([0.8, 0.0, 0.0, 0.0], "turn right"),
            ([0.8, -0.6, 0.8, 0.3], "drop an objective above "),
            ([0.8, -0.3, 0.5, -0.5], "close wrist"),
            ([-0.8, -0.3, 0.5, -0.5], "carry toward left"),
            ([-0.8, 0.0, 0.0, 0.3], "put an objective"),
            ([0.0, 0.0, 0.0, 0.0], "go back home"),
        ]

        for loop in range(2):
            for positions, label in waypoints:
                robot_action_publisher.get_logger().info(f'->{label}: {positions}')
                robot_action_publisher.move_to_position(positions)
                time.sleep(5.0)#wait for finishing movements


        robot_action_publisher.get_logger().info('finished all movements. end up...')

    except KeyboardInterrupt:
        robot_action_publisher.get_logger().info('interruptted by user')
    finally:
        robot_action_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
