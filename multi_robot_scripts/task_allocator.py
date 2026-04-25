import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import time

class TaskAllocator(Node):
    def __init__(self):
        super().__init__('task_allocator')

        # Action clients for navigation
        self.client_tb1 = ActionClient(self, NavigateToPose, '/tb1/navigate_to_pose')
        self.client_tb2 = ActionClient(self, NavigateToPose, '/tb2/navigate_to_pose')
        self.client_tb3 = ActionClient(self, NavigateToPose, '/tb3/navigate_to_pose')

        # Initial pose publishers
        self.init_pub_tb1 = self.create_publisher(PoseWithCovarianceStamped, '/tb1/initialpose', 10)
        self.init_pub_tb2 = self.create_publisher(PoseWithCovarianceStamped, '/tb2/initialpose', 10)
        self.init_pub_tb3 = self.create_publisher(PoseWithCovarianceStamped, '/tb3/initialpose', 10)

        # Initial poses matching robots.yaml positions
        self.init_poses = {
            'tb1': (-1.5, -0.5),
            'tb2': (-1.5,  0.5),
            'tb3': ( 1.5, -0.5),
        }

        # Goal zones for each robot
        self.goals = {
            'tb1': (-1.5,  1.5),
            'tb2': ( 0.0, -1.5),
            'tb3': ( 1.5,  1.5),
        }

    def set_initial_pose(self, publisher, x, y, robot_name):
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        msg.pose.pose.orientation.w = 1.0
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.07
        publisher.publish(msg)
        self.get_logger().info(f'Initial pose set for {robot_name}: ({x}, {y})')

    def send_goal(self, client, x, y, robot_name):
        self.get_logger().info(f'Waiting for {robot_name} action server...')
        client.wait_for_server()
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.orientation.w = 1.0
        self.get_logger().info(f'Sending goal to {robot_name}: ({x}, {y})')
        client.send_goal_async(goal)

    def run(self):
        # Wait for Nav2 to fully start
        self.get_logger().info('Waiting for Nav2 to start...')
        time.sleep(10)

        # Set initial poses for all robots
        self.get_logger().info('Setting initial poses...')
        for _ in range(5):
            self.set_initial_pose(self.init_pub_tb1, *self.init_poses['tb1'], 'tb1')
            self.set_initial_pose(self.init_pub_tb2, *self.init_poses['tb2'], 'tb2')
            self.set_initial_pose(self.init_pub_tb3, *self.init_poses['tb3'], 'tb3')
            time.sleep(0.5)

        # Wait for localization to settle
        self.get_logger().info('Waiting for localization to settle...')
        time.sleep(5)

        # Send navigation goals
        self.send_goal(self.client_tb1, *self.goals['tb1'], 'tb1')
        self.send_goal(self.client_tb2, *self.goals['tb2'], 'tb2')
        self.send_goal(self.client_tb3, *self.goals['tb3'], 'tb3')
        self.get_logger().info('All goals sent! Robots are navigating.')

def main():
    rclpy.init()
    node = TaskAllocator()
    node.run()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
