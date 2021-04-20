#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 15:24:44 2019

@author: michael

This script subscribes to a GPS odometry message and re publishes it if the error is within a specified threshold (mask).
It is found to ignore high error GPS data during mapping is better than fusing it.

"""

from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
import tf
from geometry_msgs.msg import Quaternion
import rospy
from math import pi, sqrt

class GpsMask:
    
    def __init__(self):

        self.gps_error_mask_std = rospy.get_param('~gps_error_mask_std', 0.1)
        self.gps_error_mask_cov = self.gps_error_mask_std**2
        
        self.gps_error_x = 0
        self.gps_error_y = 0

        self.odom_repub = rospy.Publisher('/odometry/gps/mask', Odometry, queue_size=10)
        self.yaw_repub = rospy.Publisher('/yaw/mask', Imu, queue_size=10)
        
        rospy.Subscriber('/odometry/gps', Odometry, self.odom_callback, queue_size = 10)
        rospy.Subscriber('/yaw', Imu, self.yaw_callback, queue_size = 10)



    def odom_callback(self, data):

        self.gps_error_x = data.pose.covariance[0]
        self.gps_error_y = data.pose.covariance[7]

        if (self.gps_error_x < self.gps_error_mask_cov) and (self.gps_error_y <self.gps_error_mask_cov):
            self.odom_repub.publish(data)
        else:
            rospy.logwarn("GPS error too high (x=%s, y=%s), masking. ", sqrt(self.gps_error_x), sqrt(self.gps_error_y))



    def yaw_callback(self, data):
    
        if (self.gps_error_x < self.gps_error_mask_cov and self.gps_error_y <self.gps_error_mask_cov):
            self.yaw_repub.publish(data)
            



if __name__ == '__main__':
    rospy.init_node('gps_mask', anonymous=True)
    GpsMask()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "End gps mask module"
