FROM tiryoh/ros-desktop-vnc:noetic
LABEL maintainer="L-CAS<mhanheide@lincoln.ac.uk>"
LABEL maintainer="L-CAS<25921584@lincoln.ac.uk>"

# Add repos
## LCAS repo (not available in noetic yet)
# RUN curl https://raw.githubusercontent.com/LCAS/rosdistro/master/lcas-rosdistro-setup.sh | bash -
## Gazebo
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
RUN wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

# Installing dependencies (map-server has some weird conflicts with libsdl)
RUN apt-get update; apt-get -y upgrade; \
    apt-get install -y ros-noetic-desktop-full ros-noetic-map-server

# Creating thorvald_ws
RUN mkdir -p /home/ubuntu/thorvald_ws/src
ADD Thorvald /home/ubuntu/thorvald_ws/src/Thorvald
RUN /bin/bash -c ". /opt/ros/noetic/setup.bash && \
                  rosdep install --from-paths ~/thorvald_ws/src -i -y && \
                  cd ~/thorvald_ws && catkin_make install && rm -rf ~/thorvald_ws/src/Thorvald && \
                  echo 'source ~/thorvald_ws/install/setup.bash' >> ~/.bashrc"

# Creating ros_ws
RUN mkdir -p /home/ubuntu/ros_ws/src
RUN /bin/bash -c ". ~/thorvald_ws/install/setup.bash && cd ~/ros_ws && catkin_make && \
                  echo 'source ~/ros_ws/devel/setup.bash' >> ~/.bashrc"

# copying bacchus repo
RUN cd /home/ubuntu/ros_ws/src && \
    git clone -b master --recursive https://github.com/LCAS/CMP9767M.git && \
    git clone -b teaching --recursive https://github.com/LCAS/bacchus_lcas.git

# Installing dependecies
RUN /bin/bash -c ".  ~/thorvald_ws/install/setup.bash && \
                  cd /home/ubuntu/ros_ws/src && \
                  git clone https://github.com/LCAS/depth_sensors.git && \
                  git clone https://github.com/LCAS/topological_navigation.git && \
                  git clone https://github.com/GT-RAIL/robot_pose_publisher.git && \
                  apt-get install -y ros-noetic-dwa-local-planner ros-noetic-teb-local-planner \
                  ros-noetic-velodyne-description ros-noetic-ira-laser-tools ros-noetic-move-base && \
                  apt-get -y clean"

RUN /bin/bash -c ". ~/thorvald_ws/install/setup.bash; cd ~/ros_ws; catkin_make -DCMAKE_CXX_STANDARD=17"

RUN cd /tmp && curl -fOL https://github.com/cdr/code-server/releases/download/v3.12.0/code-server_3.12.0_amd64.deb && dpkg -i code-server_3.12.0_amd64.deb && rm code-server_3.12.0_amd64.deb && /usr/bin/code-server --install-extension ms-python.python && /usr/bin/code-server --install-extension pijar.ros-snippets

RUN bash -c 'echo -e "[supervisord]\nredirect_stderr=true\nstopsignal=QUIT\nautorestart=true\ndirectory=/root\n\n[program:codeserver]\ndirectory=/home/ubuntu\ncommand=/usr/bin/code-server --auth none --bind-addr 0.0.0.0:8888\nuser=ubuntu\nenvironment=DISPLAY=:1,HOME=/home/ubuntu,USER=ubuntu,PYTHONPATH=/home/ubuntu/ros_ws/devel/lib/python3/dist-packages:/home/ubuntu/thorvald_ws/install/lib/python3/dist-packages:/opt/ros/noetic/lib/python3/dist-packages" > /etc/supervisor/conf.d/codeserver.conf'

