^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package bacchus_gazebo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.3.4 (2022-01-10)
------------------
* Merge pull request `#43 <https://github.com/LCAS/bacchus_lcas/issues/43>`_ from gcielniak/teaching
  fix global costmap parameters
* enable nav_map_yaml as a configurable parameter
* Enable non-paused sim + Fix depth camera_info topic
* Revert Niko's commit
* 'improve' the world ;)
* Contributors: Riccardo, Riccardo Polvara, gcielniak, nikostsagk

* Patched arg for move_base missing in hierarchical launch files
* Fix camera frame in camera_info topic
* Contributors: Riccardo, pulver

0.3.2 (2021-10-17 09:00)
------------------------
* changelogs
* Merge pull request `#40 <https://github.com/LCAS/bacchus_lcas/issues/40>`_ from LCAS/coarse_models
  Added new world with the coarse meshes
* Delete semantic.xacro
  This is not needed here
* Added new world with the coarse meshes
  + disable multi_sim + set the world default to the simplified models.
* Merge pull request `#39 <https://github.com/LCAS/bacchus_lcas/issues/39>`_ from pulver22/teaching-multisim
  Added support for multisim robot and various fix on tf prefix
* Fix velodyne frame and wrong robot description in rviz
* Fix test case
* Multisim seems to work + Rviz config
* Single robot does work in multisim scenario
* Working on the single robot to work in a multisim scenario
  Tf-tree looks fine but local costmap is not built and the robot is not moving
* Merge pull request `#1 <https://github.com/LCAS/bacchus_lcas/issues/1>`_ from LCAS/teaching
  Synchronise with upstream
* Merge branch 'teaching-multisim' into teaching
* Start working towards offering multisim
* Contributors: Ibrahim, Marc Hanheide, Riccardo, Riccardo Polvara, pulver

0.3.1 (2021-10-10)
------------------
* changelogs
* change defaults (for teaching only)
* added smaller worlds for teaching
* removed sprayer
* Various fix (sensor frame, local costmap, enable/disable dt)
* Contributors: Marc Hanheide, Riccardo

0.3.0 (2021-10-06)
------------------
* changelogs
* Removed actor plugin
* Cleanup Robotnik reference
* Merge pull request `#30 <https://github.com/LCAS/bacchus_lcas/issues/30>`_ from LCAS/fix_digital_twin_sim
  thorvald up and running - sherpa still pending (new pull request will be opened)
* fix issue with riseholme ground plane
* Add riseholme terrain model
  Extract riseholme terrain model from the downloaded 3D models file
* Merge remote-tracking branch 'origin/fix_digital_twin_sim' into fix_digital_twin_sim
* correct tf namespace for the kinect and velodyne
* Added missing dep (fake_localization)
* Added corner_laser_merger automatically launched after 20s
* Maintainer in Package.xml
* Re-enable riseholme map
* Cleaned main launch file
* Fix Thorvald navigation using move_base
* Refactoring launch files with individual ones for each platform
* Fix SINGLE Thorvald navigation
* Working status to fix tf-tree of simulated platforms
* Riseholme maps
* Correct Bacchus sensor suite
* Merge pull request `#27 <https://github.com/LCAS/bacchus_lcas/issues/27>`_ from pulver22/fix_launch_file
  The launch file atm is loading a broken riseholme sim, revert to standar
* Spawing Thorvald in the Riseholme field.
  Still getting the spawner to crash
* The launch file atm is loading a broken riseholme sim, revert to standar
* Merge pull request `#25 <https://github.com/LCAS/bacchus_lcas/issues/25>`_ from LCAS/riseholme-sim
  Simulated world of Riseholme with inclined terrain and fences
* Created a riseholme world compatible with data recorded by Michael
* Re-enable robot in the launch file
* Simulated world of Riseholme with inclined terrain and fences
* Merge pull request `#13 <https://github.com/LCAS/bacchus_lcas/issues/13>`_ from LCAS/heightmap_mesh
  Merging after passing CI! Hooray!
* Removed additional launch file and set heightmap as default world
* update vineyard_heightmap launch file
* adding heightmap models
* Merge pull request `#7 <https://github.com/LCAS/bacchus_lcas/issues/7>`_ from pulver22/robotnik-launch
  Merging after passing all the tests.
* Parametrised hokuyo + 2 sensors suites
  The test should now pass
* Laser merger required to fuse lidar and fix costmap generation
* Added sensors xacro dedicated files with macro
* Thorvald default platform + commented robot control part [not working]
* Single Launch file for Thorvald & Robotnik
* Contributors: Ibrahim, Marc Hanheide, Riccardo, Riccardo Polvara, Sergi Molina, ibrahim hroob, sergimolina

0.2.2 (2020-11-18 15:35)
------------------------
* changelogs
* added exec_depend for launch files
* Contributors: Marc Hanheide

0.2.1 (2020-11-18 12:07)
------------------------
* changelogs
* fix deps
* Contributors: Marc Hanheide

0.2.0 (2020-11-18 11:08)
------------------------
* changelogs
* Merge pull request `#6 <https://github.com/LCAS/bacchus_lcas/issues/6>`_ from LCAS/better_download_models
  Better build and demo
* improved the download build and also allow rviz navigation
* Contributors: Marc Hanheide

0.1.0 (2020-11-18 08:07)
------------------------
* changelogs
* Merge pull request `#5 <https://github.com/LCAS/bacchus_lcas/issues/5>`_ from LCAS/vine_stages
  Vine stages
* deleted vine_t0 model
* changed the testme.test file to pass the test with a new launch file
* Merge branch 'master' into vine_stages
* fix download directory + remove vine_t0.dae
* Auto download vineyard modes (from nextcloud) upon building the workspace (catkin_make)
* Merge pull request `#4 <https://github.com/LCAS/bacchus_lcas/issues/4>`_ from LCAS/change_sensors
  added the new kinect cameras configuration
* added the new kinect cameras configuration
* added config file rviz
* Update vineyard_demo.launch
  added rviz
* Merge pull request `#3 <https://github.com/LCAS/bacchus_lcas/issues/3>`_ from LCAS/new_sim_sergi
  adding move base and main launch file
* adding move base and main launch file
* Add vineyard simulation at stage 0
* Contributors: Ibrahim Hroob, Marc Hanheide, Sergi Molina, sergimolina

0.0.1 (2020-07-08)
------------------
* version
* changelogs
* renamed file
* changed to cmp9767m base
* removed outdated deps
* removed outdated deps
* version
* initial commit
* Contributors: Marc Hanheide
