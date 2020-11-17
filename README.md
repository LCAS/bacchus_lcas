# bacchus_lcas
A repository for contributions to the BACCHUS H2020 project

## Launch the system with:
`roslaunch bacchus_gazebo vineyard_demo.launch`

To change the world modify the "world_name" parameter inside the launch file.

## To send goals:
Go to bacchus_lcas/bacchus_move_base/scripts and run

`python send_goals.py _goals_seq_file:=../config/goals/vineyard_demo_goals.txt`

The goals_seq_file has to be a txt containing 3 columns [x,y,yaw]. They define the sequence of goals to be send top the robot.
