#!/usr/bin/env python
import math

import rospy
import tf
from nav_msgs.msg import Odometry


def callback_odom(odom):
    q = odom.pose.pose.orientation
    _, _, th = tf.transformations.euler_from_quaternion(
        (q.x, q.y, q.z, q.w))
    x = odom.pose.pose.position.x
    y = odom.pose.pose.position.y
    print(f'x:{x:.3f} y:{y:.3f} th:{math.degrees(th):.1f}')


rospy.init_node('monitor')
sub_odom = rospy.Subscriber('/odom', Odometry, callback_odom)
rospy.spin()
