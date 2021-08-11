#!/usr/bin/env python

import rospy

from nav_msgs.msg import Odometry
import tf

class remap_odom_tf():

    def __init__(self):

        # Parameters
        self.odom_topic_name = rospy.get_param("~odom_topic_name", "odom")
        self.new_odom_topic_name = rospy.get_param("~new_odom_topic_name", "new_odom")
        self.odom_frame_id = rospy.get_param("~odom_frame_id", "")
        self.base_frame_id = rospy.get_param("~base_frame_id", "")
        self.publish_tf = rospy.get_param("~publish_tf", "false")

        # Subscribers
        rospy.Subscriber(self.odom_topic_name, Odometry, self.odometry_callback)
        
        # Publishers
        self.odom_pub = rospy.Publisher(self.new_odom_topic_name, Odometry, queue_size=1)

    def odometry_callback(self, msg_data):
        odom_msg = Odometry()
        odom_msg = msg_data
        if self.odom_frame_id != "":
            odom_msg.header.frame_id = self.odom_frame_id
        if self.base_frame_id != "":
            odom_msg.child_frame_id = self.base_frame_id
        self.odom_pub.publish(odom_msg)

        if self.publish_tf:
            if (self.odom_frame_id != "") and (self.base_frame_id != ""):
                tf_br = tf.TransformBroadcaster()
                tf_br.sendTransform((odom_msg.pose.pose.position.x, odom_msg.pose.pose.position.y, 0),
                                    (odom_msg.pose.pose.orientation.x,odom_msg.pose.pose.orientation.y,odom_msg.pose.pose.orientation.z,odom_msg.pose.pose.orientation.w),
                                    rospy.Time.now(),
                                    self.base_frame_id,
                                    self.odom_frame_id)
            else:
                rospy.loginfo("Tf NOT published - You must define both odom and base frame ids")




if __name__ == '__main__':
    rospy.init_node('remap_odom_tf_node')
    rot = remap_odom_tf()
    rospy.spin()
