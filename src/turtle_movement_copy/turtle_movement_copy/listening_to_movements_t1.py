import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
from turtlesim.srv import TeleportRelative, TeleportAbsolute

class ListenToTurtle1Movements(Node):
    def __init__(self):
        super().__init__('turtle1_listener')
        self.cli = self.create_client(Spawn, '/spawn')
        self.turtle2_srv = self.create_client(TeleportRelative, '/turtle2/teleport_relative')
        self.tutrle1_srv = self.create_client(TeleportAbsolute, 'turtle1/teleport_absolute')
        self.listener = self.create_subscription(Twist, '/turtle1/cmd_vel', self.listener_callback, 10)
        self.listener
        self.req_spawn = Spawn.Request()
        self.linear_x_change = 0.0
        self.angular_z_change = 0.0

    def listener_callback(self, msg):
        self.linear_x_change = float(msg.linear.x)
        self.angular_z_change = float(msg.angular.z)
        self.send_request_copy()
        self.get_logger().info('Something happened!!!')

    def send_request_spawn(self):
        self.req_spawn.x = 3.0
        self.req_spawn.y = 5.5
        self.req_spawn.name = "turtle2"
        return self.cli.call_async(self.req_spawn)

    def send_request_copy(self):
        req_teleport = TeleportRelative.Request()
        req_teleport.linear = float(self.linear_x_change)
        req_teleport.angular = float(self.angular_z_change)
        return self.turtle2_srv.call_async(req_teleport)


def main(args=None):
    rclpy.init(args=args)
    listener = ListenToTurtle1Movements()
    listener.send_request_spawn()
    rclpy.spin(listener)
    listener.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()