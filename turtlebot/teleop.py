#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, termios, tty, select

# Max velocities
MAX_LINEAR_X = 0.21      # m/s
MAX_ANGULAR_Z = 1.9     # rad/s

# Key mapping
move_bindings = {
    'w': (MAX_LINEAR_X, 0.0),         # forward
    's': (-MAX_LINEAR_X, 0.0),        # backward
    'a': (0.0, MAX_ANGULAR_Z),        # turn left
    'd': (0.0, -MAX_ANGULAR_Z),       # turn right
    'q': (MAX_LINEAR_X/2, MAX_ANGULAR_Z/2),   # forward-left
    'e': (MAX_LINEAR_X/2, -MAX_ANGULAR_Z/2),  # forward-right
    ' ': (0.0, 0.0),                  # stop
}

class KeyboardTeleopMax(Node):
    def __init__(self):
        super().__init__('keyboard_teleop_max')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info(
            "Keyboard teleop started. WASD + QE for diagonal. Space to stop."
        )

    def get_key(self):
        """Read a single keypress"""
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def run(self):
        try:
            while rclpy.ok():
                key = self.get_key()
                if key in move_bindings:
                    linear_x, angular_z = move_bindings[key]
                    twist = Twist()
                    twist.linear.x = linear_x
                    twist.angular.z = angular_z
                    self.pub.publish(twist)
                    print(f"Published: linear.x={linear_x}, angular.z={angular_z}")
                elif key == '\x03':  # Ctrl-C
                    break
        except Exception as e:
            self.get_logger().error(str(e))

def main(args=None):
    global settings
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = KeyboardTeleopMax()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
