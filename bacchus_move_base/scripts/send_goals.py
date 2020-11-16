#!/usr/bin/env python
# license removed for brevity
import rospy
import math
import csv

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler


class MoveBaseSeq():

    def __init__(self):

        rospy.init_node('move_base_sequence')
        self.goals_seq_file = rospy.get_param('~goals_seq_file',"../vineyard_demo_goal.txt")
        self.x_seq = []
        self.y_seq = []
        self.yaw_seq = []
        self.num_goals = 0

        with open(self.goals_seq_file) as ifile:
            ifile_data = csv.reader(ifile, delimiter=',')
            for line in ifile_data:
                self.x_seq.append(float(line[0]))
                self.y_seq.append(float(line[1]))
                self.yaw_seq.append(float(line[2]))
                self.num_goals = self.num_goals + 1

        self.goal_cnt = 0
        #Create action client
        self.client = actionlib.SimpleActionClient('thorvald_001/move_base',MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        wait = self.client.wait_for_server(rospy.Duration(5.0))
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            return
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting goals achievements ...")
        self.movebase_client()

    def active_cb(self):
        rospy.loginfo("Goal pose "+str(self.goal_cnt+1)+" is now being processed by the Action Server...")

    def feedback_cb(self, feedback):
        #To print current pose at each feedback:
        #rospy.loginfo("Feedback for goal "+str(self.goal_cnt)+": "+str(feedback))
        rospy.loginfo("Feedback for goal pose "+str(self.goal_cnt+1)+" received")

    def done_cb(self, status, result):
        self.goal_cnt += 1
    # Reference for terminal status values: http://docs.ros.org/diamondback/api/actionlib_msgs/html/msg/GoalStatus.html
        if status == 2:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request after it started executing, completed execution!")

        if status == 3:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" reached") 
            if self.goal_cnt< self.num_goals:
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now() 

                goal.target_pose.pose.position.x = self.x_seq[self.goal_cnt]
                goal.target_pose.pose.position.y = self.y_seq[self.goal_cnt]

                ox,oy,oz,ow = quaternion_from_euler(0, 0, self.yaw_seq[self.goal_cnt]*math.pi/180)
                goal.target_pose.pose.orientation.x = ox
                goal.target_pose.pose.orientation.y = oy
                goal.target_pose.pose.orientation.z = ow
                goal.target_pose.pose.orientation.w = oz        

                rospy.loginfo("Sending goal pose "+str(self.goal_cnt+1)+" to Action Server")
                self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)
            else:
                rospy.loginfo("Final goal pose reached!")
                rospy.signal_shutdown("Final goal pose reached!")
                return

        if status == 4:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" was aborted by the Action Server")
            rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" aborted, shutting down!")
            return

        if status == 5:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" has been rejected by the Action Server")
            rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" rejected, shutting down!")
            return

        if status == 8:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request before it started executing, successfully cancelled!")

    def movebase_client(self):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now() 

        goal.target_pose.pose.position.x = self.x_seq[self.goal_cnt]
        goal.target_pose.pose.position.y = self.y_seq[self.goal_cnt]

        ox,oy,oz,ow = quaternion_from_euler(0, 0, self.yaw_seq[self.goal_cnt]*math.pi/180)
        goal.target_pose.pose.orientation.x = ox
        goal.target_pose.pose.orientation.y = oy
        goal.target_pose.pose.orientation.z = ow
        goal.target_pose.pose.orientation.w = oz        

        rospy.loginfo("Sending goal pose "+str(self.goal_cnt+1)+" to Action Server")
        self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)
        rospy.spin()

if __name__ == '__main__':
    try:
        MoveBaseSeq()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")