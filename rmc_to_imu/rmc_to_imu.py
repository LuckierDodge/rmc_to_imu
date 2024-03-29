import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from nmea_msgs.msg import Sentence

from geometry_msgs.msg import Quaternion
from tf_transformations import quaternion_from_euler
from mcity_proxy_msgs.msg import Heading

import math
import numpy as np


class Rmc_To_Imu(Node):
    def __init__(self):
        super().__init__("rmc_to_imu")

        self.heading_publisher_ = self.create_publisher(Heading, "/heading", 10)
        self.imu_publisher_ = self.create_publisher(Imu, "/imu/heading", 10)
        self.nmea_subscriber_ = self.create_subscription(
            Sentence, "nmea", self.nmea_callback, 10
        )
        self.timer = self.create_timer(1, self.timer_callback)
        self.last_msg = None

    def nmea_callback(self, msg):
        sentence = msg.sentence
        if "RMC" in sentence:
            split = sentence.split(",")
            cog = split[8]
            # self.get_logger().info(f"{split}")
            if cog != "":
                self.last_msg = msg
                heading = -1.0 * math.radians(float(cog)) + (np.pi / 2.0) # * Convert to Radians ENU
                while heading > 2.0 * np.pi:
                    heading -= 2.0 * np.pi
                while heading < 0.0:
                    heading += 2.0 * np.pi

                msg = Heading(heading=heading)
                self.heading_publisher_.publish(msg)
                q = quaternion_from_euler(
                    0,
                    0,
                    heading
                )
                msg = Imu(orientation=Quaternion(x=q[0], y=q[1], z=q[2], w=q[3]))
                msg.header.frame_id = "gps"
                self.imu_publisher_.publish(msg)
                # self.get_logger().info(f"{cog}, {float(cog) * 3.1415926535 / 180}, ({q[2]}, {q[3]})")

    def timer_callback(self):
        if self.last_msg is not None:
            self.nmea_callback(self.last_msg)


def main(args=None):
    rclpy.init(args=args)

    rmc_to_imu = Rmc_To_Imu()
    rclpy.spin(rmc_to_imu)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    rmc_to_imu.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
