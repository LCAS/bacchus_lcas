# bacchus_lcas
A repository for contributions to the BACCHUS H2020 project

=======
## 1 - Getting the system
1. Go to ~/catkin_ws/src and clone the repo: `git clone https://github.com/LCAS/bacchus_lcas.git`
1. While inside ~/catkin_ws/src , install all dependencies for the packages with: `rosdep install --from-paths . -i`
1. Go to ~/catkin_make and compile: `catkin_make`


## 2 - Launch the system with:
`roslaunch bacchus_gazebo vineyard_demo.launch`

To change the world you can modify the "world_name" parameter inside the launch file.

### (optional)  Manual teleoperation of thorvald
At this stage, you should be able to control manually the robot with the keyboard.
To do so run:
`rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=/thorvald_001/nav_vel`


## 3 - To send a sequence of goals:
Go to ~/catkin_ws/src/bacchus_lcas/bacchus_move_base/scripts and run:

`python send_goals.py _goals_seq_file:=../config/goals/vineyard_demo_goals.txt`

The `goals_seq_file` has to be a txt containing 3 columns [x,y,yaw]. They define the sequence of goals to be send to the robot.
