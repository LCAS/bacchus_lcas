^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package rasberry_move_base
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.1.0 (2018-11-02)
------------------
* Merge remote-tracking branch 'upstream/master'
* Merge pull request `#149 <https://github.com/LCAS/RASberry/issues/149>`_ from gpdas/master
  Merging this. Package for autonomous UV treatment - initial commits
* uv_treatment simulation cleanup
  1. costmap - inflation radius reduced to 0.5
  2. topo_map for riseholme-uv_sim added
  3. scenario sim_riseholme-uv.sh updated with new TMAP and MAP values
  4. cleanup in uv_treatment.py
* cleanup and merging latest changes in master to uv related parameters
* Merge branch 'uv' of github.com:gpdas/RASberry into uv
* Merge branch 'master' of github.com:LCAS/RASberry into uv
* Merge pull request `#145 <https://github.com/LCAS/RASberry/issues/145>`_ from adambinch/master
  Merging this. costmap parameter modified and topo_map adjustment.
* Adjusted some of the costmap and local planner params (these were confirmed to work during a practical session with the robot at Riseholme.)
  Shifted end row nodes in topo map by 4cm in y direction. Adjusted position of node 10 in topo map for simulation.
* added new set of DWAPlannerRos parameters for uv treatment scenario
* Merge branch 'master' into master
* Merge pull request `#134 <https://github.com/LCAS/RASberry/issues/134>`_ from Jailander/master
  Looks good. Merging this. Adding the possibility to use carrot planner for the uv scenario
* Adding the possibility to use carrot planner for the uv scenario
* Merge branch 'master' of https://github.com/LCAS/RASberry
* WIP: riseholme development (`#121 <https://github.com/LCAS/RASberry/issues/121>`_)
  * added riseholme maps and uk robot 007 config files
  * .yaml and .tmap for riseholme topological map
  * more univeraal launch files
  * added scenario and more flexible tmule script
  * no sleeps necessary with new tmule
  * rise.pgm added
  * with topological nodes now
  * rise.pgm added
  * updated sensor measurements for switch to 008 frame
  * Added a script to start mapping
  * Added running IMU in start mapping script
  * Made start mapping script executable
  * tmap with charging, storage and base station
  * Cropping riseholme 2d map
  1. riseholme 2d map is cropped. Use riseholme.yaml with map_server.
  2. modified existing riseholme.tmap to riseholme_sim.tmap for the topological map for gazebo simulation
  3. added riseholme.tmap (a modified version of rise.tmap) to be used with riseholme.yaml 2D map.
  4. start_sim_risholme_unified.sh is updated to use riseholme_sim pointset from mongodb
  The above changed will make rise.yaml, rise.pgm, and rise.tmap deprecated. They are retained in this commit.
  * Robot objects in coordination now subscribes to robot_pose topics
  1. robot_pose topic is subscribed by the robot objects
  2. robot_pose is also used now for localising the robot in the topological map. this is to avoid low updates of the latched topic (closest_node) when used with rosbridge and rosduct interface.
  3. threading.Lock object is used to do the closest_node updates from two callbacks thread safe
  4. package and CMakeList are updated with rasberry_people_perception as additional dependency (for topological_localiser)
  * Removing the country prefix to robot config and sensor frame xacro
  * riseholme config fixes
  * Updated 2D map with FH building
  robot_007_sensors.xacro gazebo-hokuyo sensing range is modified to -135 to 85 degrees
  * adopted for server
  * SCENARIO_NAME is used for coordination config file in tmule config
  map_config_riseholme.yaml modified with nodes from the latest riseholme tmap.
  * load local config
  * fix for idle_robots without have topo_nav ready robots
  if a robot_name is in the map_config_scenario.yaml file, it was assumed to be idle. If the physical/simulated robot was not initialised its closest_node would be "none" and therefore wouldn't be considered while closest_robot to a task. now such robots wont be added to idle_robots and therefore tasks won't be removed from Queue unnecessarily.
  * New riseholme no_go map (with FH unit building)
  * local changes
  * added marvel and no go
  * shifted the map globally by 10cm!
  * some simple nav parameters that worked better, not great though
  * self.pose not to be updated from _update_closest_cb
  * added cache for topological_map (if server becomes unavailable)
  * fix for picker_node being None in add_task
  1. The actual fix is in picker_state_monitor, where the picker nodes are
  intialised as "none" now rather than None
  2. picker_marvel_localiser now checks for "none" rather than None before
  publishing closest and current nodes
  3. coordinator and robot in rasberry_coordination need values for
  static_nodes (storage etc) of the map.
  * fix: Task not added if picker is not localised
  1. If a picker who is not localised in the topomap is calling a robot, it is ignored and the callarobot state of the picker is reset to INIT
  2. fix in threading.Lock() usage for closest_node of robots
  3. fix for self._topo_nav.get_result() giving None
  * don't run picker localisation in robot
  * persistent topics updated
  * laser position centred
  * added .rasberryrc example file
  * angles shifted for center laser
  * params from riseholme demo
* Merge pull request `#120 <https://github.com/LCAS/RASberry/issues/120>`_ from gpdas/master
  Merging this. Post Noway workshop demo Cleanup
* fix rasberry_move_base package.xml and CMakeLists.txt
* CMakeLists.txt and package.xml updated with dependencies and install targets
* Post Noway workshop demo Cleanup
  1. deleted:    rasberry_bringup/launch/rasberry_simulation.launch. Use robot_brinup.launch.
  2. multi-robot simulations: This is not our current focus, however keeping these updated with other developments.
  - deleted:    rasberry_bringup/launch/rasberry_simulation_multi.launch. Use robot_bringup_multisim.launch (new file)
  - new file:   rasberry_move_base/launch/move_base_dwa_multisim.launch
  - renamed:    rasberry_move_base/launch/move_base_teb_multi.launch -> rasberry_move_base/launch/move_base_teb_multisim.launch
  - renamed:    rasberry_bringup/scripts/start_sim_multi.sh -> rasberry_bringup/scripts/start_multisim.sh
  3. all maps are now removed from rasberry_gazebo. already moved all maps to rasberry_navigation
  - modified:   rasberry_bringup/launch/rasberry_simulation_velo_k2.launch
  - modified:   rasberry_gazebo/launch/actor_move_base_dwa.launch
  - deleted:    rasberry_gazebo/maps/*
  - modified:   rasberry_move_base/launch/map_server.launch
  - modified:   rasberry_people_perception/launch/ultrasonic_localisation.launch
  4. deleted:    rasberry_bringup/launch/thorvald_realtime.launch. Use robot_brinup.launch.
  5. new file:   rasberry_bringup/urdf/norway_robot_003_sim_sensors.xacro.
  - Modified of the xacro on thorvald_003 for norway_poles demo.
  - In simulation, the coordiate frames of hokuyo is not right (some rays are hitting the robot itself with 180 degree view)
  6. shell script updates (before tmule configs to test things, these are used).
  - modified:   rasberry_bringup/scripts/start_sim.sh
  - renamed:    rasberry_bringup/scripts/start_sim_multi.sh -> rasberry_bringup/scripts/start_multisim.sh (multi-robot simulation. only upto move_base)
  - modified:   rasberry_bringup/scripts/start_sim_norway_poles_unified.sh. This can be used to simulate norway_poles scenario with one robot and multiple pickers from a single roscore
  - modified:   rasberry_bringup/scripts/start_sim_riseholme_unified.sh. This can be used to simulate riseholme_sim scenario with one robot and multiple pickers from a single roscore
  7. modified:   rasberry_bringup/tmule/norway_poles_sim.yaml.
  - changes in tmule configs from robot.
  - ROBOT_NAME by truncating "-" from hostname, mongodb directory and launch, and reduced sleep delays.
  - not tested, but could be modified in future for simulating the scenarios with multi-roscore as in real cases with rosduct. Keeping updated along with other changes.
  8. modified:   rasberry_move_base/launch/move_base_dwa.launch. remapping odom to odometry/base_raw
  9. coorindation/scheduling related:
  - new file:   rasberry_coordination/config/map_config_riseholme_sim.yaml. Configuration file to be used with simple_task_executor_node for riseholme_sim scenario.
  - modified:   rasberry_coordination/scripts/simple_task_executor_node.py. Now passes "unified" parameter to PickerStateMonitor as well.
  - modified:   rasberry_coordination/src/rasberry_coordination/coordinator.py.
  - when "unified" is true (single roscore) only one robot will be added due to the base namespacing of many topological navigation topics.
  - now checks for start and goal nodes being "none"
  - now checks for route is None while getting route to picker (to find the nearest robot). None could come if there is no possible path.
  - minor rosinfo msg updates
  - modified:   rasberry_coordination/src/rasberry_coordination/picker_state_monitor.py
  - now takes "unified" status and when it is true, assumes there is only one robot
  - modified:   rasberry_coordination/src/rasberry_coordination/robot.py
  - minor rosinfo msg updates
  - fixed some bugs in checking topo_nav action goal status.
  - Known issues (to be investigated later):
  - collectTray goal is cancelled, if any topo_nav action goal underneath is aborted or recalled by the action server. It is still not elegant way of doing it, as there could be better feedback.
  - if there is only one idle robot and a path does not exist from the robot to the picker, the collecttray task is still assigned to that robot. this should be avoided.
  - with riseholme.tmap, some nodes could be used in rviz to set top_nav goals, same nodes when used to find a path, failed as well as those tasks were aborted/recalled (?)
* Merge pull request `#1 <https://github.com/LCAS/RASberry/issues/1>`_ from LCAS/master
  sync with LCAS
* Merge pull request `#104 <https://github.com/LCAS/RASberry/issues/104>`_ from gpdas/norway_rob_cfg
  Merging this. Mostly updatign Norway robot model dimensions and move_base parameters.
* Norway robot configuration changes
  1. Robot dimensions adjusted -> rasberry_bringup/config/norway_robot.yaml
  2. sensor frames corrected -> rasberry_bringup/urdf/norway_robot_sensors.xacro
  3. robot_bringup.launch is added to bring the robot up (physical or simulated)
  4. rasberry_bringup/scripts/start_sim.sh modified with latest launch files
  5. move_base parameters adjusted to the ones used in the robot, including a new global_obstacle_layer in which laser scan is not used for marking/clearing costmap.
* Merge branch 'master' into people_perception
* Merge branch 'master' of github.com:LCAS/RASberry
* Merge pull request `#99 <https://github.com/LCAS/RASberry/issues/99>`_ from adambinch/master
  Merging this. this corrects some parameter configuration errors. Some more parameter tunings should be coming later from the navigation testing team - after testings.
* Changed params of local inflation to be the same as for global inflation in rasberry_move_base/config/costmap_common_params.yaml
* Indented the plugins section of rasberry_move_base/local_costmap_params.yaml and changed
  - {name: laser_scan_sensor, type: "costmap_2d::ObstacleLayer"}
  to
  - {name: obstacle_layer, type: "costmap_2d::ObstacleLayer"}.
  Also changed
  - {name: obstacle_layer, type: "costmap_2d::VoxelLayer"} in rasberry_move_base/global_costmap_params.yaml
  to
  - {name: obstacle_layer, type: "costmap_2d::ObstacleLayer"}
  and
  - {name: inflation, type: "costmap_2d::InflationLayer"}
  to
  - {name: global_inflation_layer, type: "costmap_2d::InflationLayer"}
* Merge branch 'master' of github.com:LCAS/RASberry
* Merge pull request `#97 <https://github.com/LCAS/RASberry/issues/97>`_ Now using seperate map_server.launch with no_go_map
  Merging this.
  Cleaningup of launch files - this pr separates `amcl` and `map_server` from `move_base` launch files. A separate launch file is already there for `amcl` and a map_server launch file (modified in this PR) in rasberry_move_base.
* Merge pull request `#1 <https://github.com/LCAS/RASberry/issues/1>`_ from gpdas/pr97
  @YiannisMenex merging some additional changes in the movebase launch files
* further changes in movebase launch files
  1. amcl, map_server are no longer launched from any of the movebase launch files
  2. norway_topo_nav.launch is removed - should be replaced with a tmule config in future
* Now using seperate map_server.launch with no_go_map
  -Removed map_server from move_base_dwa.launch (+ the needed arguments)
  -Editted the map_server.launch to also include the no_go_map
  -Added the no_go_map file (pgm + yaml) in rasberry_gazebo/maps
  -New layer "no_go_layer" in costmap_common_params.yaml
  -Added the no_go_map layer ("no_go_layer") in global_costmap
* Multi thorvald simulations (`#85 <https://github.com/LCAS/RASberry/issues/85>`_)
  * Multi thorvald simulations
  Lauch files for multiple thorvalds added. The launch files launch two robots in their own namespaces. move_base works for both robots. This needs [Thorvald repo commit f73668c](https://github.com/LCAS/Thorvald/commit/f73668c280685e989d29a996693662058d16eec6) to work!
  1. thorvalds are named as `thorvald_001` and `thorvald_002`.
  2. Only move_base with teb local planner is tested.
  3. Similar to earlier simulations instructions, run start_sim.sh to start tmux session for this.
  4. map_server is moved out from move-base-teb launcher to an independent launch file
  * Fixed an issue with robot_pose_publisher not publishing
  1. robot_pose_publisher is launched from move_base launch files now, earlier it was in amcl.launch
  2. frames are properly set for robot_pose_publisher to publish robot_pose topics correctly
  * XORG DISPLAY is set to 0 now
  It was set to 1 earlier for my laptop.
  * Revert "Fixed an issue with robot_pose_publisher not publishing"
  This reverts commit e9ecad2c7a0ef35b1131958bb95f74b8910a78e7.
  * XORG DISPLAY is set to 0 now
  *  Fixed an issue with robot_pose_publisher not publishing
  1. robot_pose_publisher is launched from move_base launch files now, earlier it was in amcl.launch
  2. frames are properly set for robot_pose_publisher to publish robot_pose topics correctly
  * Multi-robot simulation setting initial pose in amcl
* Multi-robot simulation setting initial pose in amcl
* Merge branch 'master' of github.com:LCAS/RASberry
* Norway topo-nav for simulation (`#89 <https://github.com/LCAS/RASberry/issues/89>`_)
  * Norway topo-nav for simulation
  The launch file that launches everything is the rasberry_navigation/launch/norway_topological_navigation.launch.
  MongoDB must be launched before launching this file, using ''rosparam set use_sim_time true''.
  Norway simulation files for topo-nav also created (amcl, costmap, move_base, norway_world.launch, new map/tmap/yaml files)
  * Removed mongoDB
  * Exposed params on existing launch files for topo-nav
  -Created new launch file that launches the topological navigation, with arguments "db_path" and "topo_map".
  -Removed duplicate files and exposed some parameteres of the already existing launch files.
  *Launch files with exposed args:
  -rasberry_bringup rasberry_simulation.launch
  -rasberry_gazebo world.launch (switched world_name from "value" to "default")
  -rasberry_move_base amcl.launch
  -rasberry_move_base move_base_dwa.launch
* Fixed an issue with robot_pose_publisher not publishing
  1. robot_pose_publisher is launched from move_base launch files now, earlier it was in amcl.launch
  2. frames are properly set for robot_pose_publisher to publish robot_pose topics correctly
* Revert "Fixed an issue with robot_pose_publisher not publishing"
  This reverts commit e9ecad2c7a0ef35b1131958bb95f74b8910a78e7.
* nw
* new_work
* Fixed an issue with robot_pose_publisher not publishing
  1. robot_pose_publisher is launched from move_base launch files now, earlier it was in amcl.launch
  2. frames are properly set for robot_pose_publisher to publish robot_pose topics correctly
* Multi thorvald simulations
  Lauch files for multiple thorvalds added. The launch files launch two robots in their own namespaces. move_base works for both robots. This needs [Thorvald repo commit f73668c](https://github.com/LCAS/Thorvald/commit/f73668c280685e989d29a996693662058d16eec6) to work!
  1. thorvalds are named as `thorvald_001` and `thorvald_002`.
  2. Only move_base with teb local planner is tested.
  3. Similar to earlier simulations instructions, run start_sim.sh to start tmux session for this.
  4. map_server is moved out from move-base-teb launcher to an independent launch file
* First commit for topoNav testcases
* Merge pull request `#74 <https://github.com/LCAS/RASberry/issues/74>`_ from adambinch/master
  Implemented move_base nav for multiple actors
* w.i.p.
* Changes for testing (not to be merged)
* Contributors: Gautham P Das, Jaime Pulido Fentanes, Johnmenex, LCASABU02, Marc Hanheide, ThomasDegallaix, Tuan Le, Yiannis Menexes, adambinch, gpdas

0.0.4 (2018-07-18)
------------------

0.0.3 (2018-07-16)
------------------
* equal versions
* adding robot pose publisher to move_base launch file
* Removing unused files
* Added more Local Planners -> check description
  *EBand Local Planner
  -Launch file: "move_base_eband.launch"
  -Parameters under directory "rasberry_move_base/config/eband/"
  *Teb Local Planner
  -Launch file: "move_base_teb.launch"
  -Parameters under directory "rasberry_move_base/config/teb/"
  *DWA Local Planner
  -Launch file: "move_base_dwa.launch"
  -Parameters under directory "rasberry_move_base/config/dwa/"
* latest move _base configs
* rasberry_move_base config files
* adding rasberry_move_base_package
* Contributors: Jaime Pulido Fentanes, Johnmenex, Marc Hanheide

* equal versions
* adding robot pose publisher to move_base launch file
* Removing unused files
* Added more Local Planners -> check description
  *EBand Local Planner
  -Launch file: "move_base_eband.launch"
  -Parameters under directory "rasberry_move_base/config/eband/"
  *Teb Local Planner
  -Launch file: "move_base_teb.launch"
  -Parameters under directory "rasberry_move_base/config/teb/"
  *DWA Local Planner
  -Launch file: "move_base_dwa.launch"
  -Parameters under directory "rasberry_move_base/config/dwa/"
* latest move _base configs
* rasberry_move_base config files
* adding rasberry_move_base_package
* Contributors: Jaime Pulido Fentanes, Johnmenex, Marc Hanheide

0.0.2 (2018-05-21)
------------------

0.0.1 (2018-03-05)
------------------
