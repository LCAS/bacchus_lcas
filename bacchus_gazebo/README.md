**bacchus_gazebo**
------------

Author: Adam Binch

email: adambinch@gmail.com

This package allows the generation of a Gazebo world with polytunnels and human models ('actors').
You can generate n polytunnels of arbitrary length positioned wherever you like in the Gazebo world.
The constraint is that the polytunnels are always aligned with the x-axis. Also, the polytunnel canopy is of a set width.
The package also permits the inclusion of n actors moving between user-specified waypoints.

# How to install:
1. Install ROS kinetic
 Follow instructions on http://wiki.ros.org/kinetic/Installation/Ubuntu
2. Setup your catkin workspace
 Follow Instructions on http://wiki.ros.org/catkin/Tutorials/create_a_workspace
3. Add LCAS ubuntu repository:
add "deb http://lcas.lincoln.ac.uk/ubuntu/main xenial main" to /etc/apt/sources.list
run `$ sudo apt update`
4. Clone RASberry repository into catkin/src folder
`$ cd ~/catkin_ws/src`
`$ git clone git@github.com:LCAS/RASberry.git`
5. Install dependencies `$ sudo apt install ros-kinetic-strands-navigation ros-kinetic-marvelmind-nav ros-kinetic-cob-generic-can ros-kinetic-twist-mux ros-kinetic-joy ros-kinetic-amcl ros-kinetic-fake-localization ros-kinetic-razor-imu-9dof ros-kinetic-robot-localization ros-kinetic-controller-manager ros-kinetic-serial python-xmltodict`

# How to build a world:
Before doing this you should have a look at the config files `./config/gazebo/models_AB.yaml` and `./config/gazebo/actors_AB.yaml`.
Also, follow steps 1-3 only if you wish to build your own world. If you do not (i.e. if you want to use one that has already been built) then proceed to step 4. <br /> 
To build a world open a terminal and do the following:

1. `roscd bacchus_gazebo/`
2. `chmod a+x ./scripts/generate_world.py`
3. `./scripts/generate_world.py --model_file ./config/gazebo/models_AB.yaml --actor_file ./config/gazebo/actors_AB.yaml`

4. If you have the Thorvald repo (https://github.com/LCAS/Thorvald) installed on your machine you can spawn the Thorvald robot model into the Gazebo World: <br /> 
`roslaunch bacchus_bringup robot_bringup.launch robot_model:=$(rospack find bacchus_bringup)/config/robot_007.yaml model_extras:=$(rospack find bacchus_bringup)/urdf/robot_007_sensors.xacro simple_sim:=true world_name:=riseholme with_actors:=false`

If you do not then:

5. `roslaunch bacchus_gazebo world.launch`

Note : you can subsitute `models_AB.yaml` and `actors_AB.yaml` in step 3 for your own config files. 
       you can use other cofiguration files in place of `robot_007.yaml` and `robot_007_sensors.xacro` in step 4.

An issue with the actors (which we will call 'type-1 actors') generated using the config file `./config/actors_AB.yaml` is that they cannot be controlled during simulation time.
Therefore another type of actor ('type-2 actor') is available in this package that can be controlled at runtime. These are robots with a human mesh, controlled with the standard 
`libgazebo_ros_planar_move` plugin. Two examples are spawned in the launch file `./launch/include_actors.launch`. Here you can set the actor's name `actor_name` and starting pose.

# Actor Move-Base
Move base has been implemented for the type-2 actors, and is applied automatically for each actor specified in `./launch/include_actors.launch`. The procedure is as follows.
1. Launch a Gazebo world (see steps 4 and 5 in the previous section). <br />
2. Launch the map server. It is recommended you use a no go map, for the given map of the environment: <br /> `roslaunch bacchus_navigation map_server.launch map:="$(rospack find bacchus_navigation)/maps/riseholme_sim.yaml" use_no_go_map:=true no_go_map:="$(rospack find bacchus_navigation)/maps/riseholme_sim_no_go.yaml"`. 
3. Include the actors: <br /> `roslaunch bacchus_gazebo include_actors.launch`.


# Info:
Open `./models_AB.yaml` for an example polytunnel configuration (there are a couple of other models that you can include as well as the polytunnels). 
Open `./actors_AB.yaml` for an example of how to include type-1 actors in the Gazebo world.

You will need to tell Gazebo to look for the models in `./models`. One way of doing this is to add the 
following to your bashrc file: `export GAZEBO_MODEL_PATH=~/path_to_bacchus_gazebo/bacchus_gazebo/models:$GAZEBO_MODEL_PATH`. 
For my machine: `export GAZEBO_MODEL_PATH=~/bacchus_ws/src/RASberry/bacchus_gazebo/models:$GAZEBO_MODEL_PATH`.

You will probably need a mid-range GPU or better to run this simulation properly.

Python package dependencies: argparse, xmltodict, rospkg, numpy, itertools, copy, json, yaml
# To do:
Possibly integrate this physical simulation with the discrete event simulation (https://github.com/LCAS/RASberry/tree/master/bacchus_des).


