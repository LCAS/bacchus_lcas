#! /usr/bin/env python
import os
import rospy
import sys
import math
import numpy as np
import yaml

import actionlib
import std_srvs

from strands_navigation_msgs.msg import TopologicalMap
from std_srvs.srv import Trigger, TriggerResponse
from std_srvs.srv import SetBool


import topological_navigation.msg

from geometry_msgs.msg import Pose, PoseWithCovarianceStamped



class FollowWaypoints(object):

    def __init__(self) :

        # Action client
        rospy.loginfo("Creating topological navigation action client ...")
        self.client = actionlib.SimpleActionClient('topological_navigation', topological_navigation.msg.GotoNodeAction)

        # Ros params
        self.topo_map = rospy.get_param('/topological_map_name','none')
        self.loop= rospy.get_param('~loop', False)
        use_homing = rospy.get_param('~use_homing', False)
        waypoints_file = rospy.get_param('~waypoints_file')
        continue_= rospy.get_param('~continue',False)

        # Useful variables
        self.waypoints_completed = False
        self.cancel=False
        self.robot_pose = None
        self.current_goal_node=None
        self.topo_map_dict = None
        self.rec_map = False


        # Subscribers
        rospy.Subscriber('/robot_pose', Pose, self.robot_pose_cb)
        rospy.Subscriber("/topological_map", TopologicalMap, self.topological_map_cb)

        # Toponav server
        rospy.loginfo("Waiting for Topological Navigation server ...")
        self.client.wait_for_server()
        rospy.loginfo(" ... Init done")

        # Get the topological map.
        rospy.loginfo("Waiting for Topological map ...")
        while not self.rec_map:
            rospy.sleep(rospy.Duration.from_sec(0.1))
        rospy.loginfo("Topological map received.")

        # Get waypoints
        wplist = self.open_waypoint_list(waypoints_file)

        # Check for continued waypoint following
        if continue_:
            rospy.loginfo("Continuing waypoint following, getting robot pose first...")
            self.robot_pose = rospy.wait_for_message('/robot_pose', Pose)
            dists = []
            for wp in wplist:
                _, dist = self.near_node(wp["node"])
                dists.append(dist)
            rospy.logwarn("Continuing waypoint following from {}".format(wplist[np.argmin(dists)]["node"]))
            wplist = wplist[np.argmin(dists):]

        print wplist
        self.wplist = wplist

        rospy.on_shutdown(self._on_node_shutdown)

        rospy.loginfo("Starting waypoints following")
        # Home wheels at start
        if use_homing:
            self.home_wheels()

        while not self.cancel:
            self.index = 0
            while self.index < len(wplist):
                wp = wplist[self.index]
                self.current_goal_node=wp['node']

                if use_homing and wp.has_key('home_wheels'):
                    if wp['home_wheels']:
                        self.home_wheels()

                success = self.navigate_to_waypoint(wp['node'])
                if success:
                    self.index+=1
                    if self.index == len(self.wplist)-1:
                        self.waypoints_completed = True

                if self.cancel:
                    break

            if not self.loop:
                self.cancel=True





    def home_wheels(self):
        rospy.wait_for_service('/base_driver/home_steering')
        try:
            activate_service = rospy.ServiceProxy('/base_driver/home_steering', Trigger)
            resp1 = activate_service()
            print(resp1.message)
            return resp1.success
        except rospy.ServiceException, e:
            print("Service call failed: %s"%e)


    def topological_map_cb(self, msg):
        self.topo_map_dict = msg
        self.rec_map = True


    def near_node(self, node_id):
        resp = False
        dist = None
        for node in self.topo_map_dict.nodes:
            if node.name == node_id:
                x = self.robot_pose.position.x
                y = self.robot_pose.position.y

                x_node = node.pose.position.x
                y_node = node.pose.position.y

                dist = np.sqrt((x-x_node)**2 + (y-y_node)**2)
                if dist <= 2.0:
                    resp = True

                break

        return resp, dist


    def robot_pose_cb(self, msg):
        self.robot_pose = msg


    def open_waypoint_list(self, waypoints_file):
        with open(waypoints_file, 'r') as listf:
            try:
                wplist = yaml.safe_load(listf)
            except yaml.YAMLError as exc:
                print(exc)
        return wplist


    def navigate_to_waypoint(self, goal):
        print "Requesting Navigation to %s" %goal
        navgoal = topological_navigation.msg.GotoNodeGoal()
        navgoal.target = goal
        navgoal.no_orientation = True

        # Sends the goal to the action server.
        self.client.send_goal(navgoal)
        # Waits for the server to finish performing the action.
        self.client.wait_for_result()
        # Prints out the result of executing the action
        ps = self.client.get_result()
        print ps

        if ps.success:
            return True
        else:
            return False


    def _on_node_shutdown(self):
        self.client.cancel_all_goals()
        self.cancel=True



if __name__ == '__main__':
    rospy.init_node('follow_waypoints')
    FollowWaypoints()

