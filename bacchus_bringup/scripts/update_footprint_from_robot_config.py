#!/usr/bin/env python
import rospy
import rospkg
import itertools
import ruamel.yaml
import sys

file_name = "/config/robots/robot_" + sys.argv[1] + "/robot_" + sys.argv[1] + "_footprint.yaml"

length_from_drive = 0.23 #meters
width_from_drive = 0.20

def init():
    rospy.init_node('update_footprint')

    rospack = rospkg.RosPack() # get an instance of RosPack with the default search paths
    pkg_path = rospack.get_path('bacchus_bringup') # get the file path
    file_path = pkg_path + file_name

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        if rospy.has_param('motor_drives'):
            base_link_to_drives = []

            for i in range(4):
                X = rospy.get_param('motor_drives/drive' + str(i) + '/x')
                Y = rospy.get_param('motor_drives/drive' + str(i) + '/y')
                base_link_to_drives.append([X,Y])

            rospy.delete_param('motor_drives')
            rospy.delete_param('batteries')
            rospy.delete_param('pipes')
            rospy.delete_param('corners')

            dimensions_from_drives = [[1 for i in range(2)] for i in range(4)]

            for i,j in itertools.product(range(4),range(2)):
                if base_link_to_drives[i][j] < 0:
                        dimensions_from_drives[i][j] = -1
                if not j:
                    dimensions_from_drives[i][j] *= length_from_drive
                else:
                    dimensions_from_drives[i][j] *= width_from_drive

            robot_dimensions = [[1 for i in range(2)] for i in range(4)]

            for i,j in itertools.product(range(4),range(2)):
                robot_dimensions[i][j] = base_link_to_drives[i][j] + dimensions_from_drives[i][j]
                robot_dimensions[i][j] = round(robot_dimensions[i][j], 5)

            footprint = {'footprint': robot_dimensions}

            ruamel.yaml.round_trip_dump(footprint, open(file_path,'w'), default_flow_style=True)

            rospy.loginfo("output is written to " + file_path)
            break
        rate.sleep()

if __name__ == '__main__':
    try:
        init()
    except rospy.ROSInterruptException:
        pass
