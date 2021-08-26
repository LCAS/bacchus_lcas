FROM tiryoh/ros-desktop-vnc:melodic

RUN apt-get update; apt-get -y upgrade

# Add repos
## LCAS
RUN curl https://raw.githubusercontent.com/LCAS/rosdistro/master/lcas-rosdistro-setup.sh | bash -
## Gazebo
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
RUN wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

RUN apt-get update; apt-get -y upgrade


# Get GTSAM and depen for LIO-SAM
RUN apt-get install -y ros-melodic-navigation ros-melodic-robot-localization ros-melodic-robot-state-publisher libjansson-dev libboost-dev imagemagick libtinyxml-dev mercurial cmake build-essential

RUN apt-get install unzip \
   && wget -O gtsam.zip https://github.com/borglab/gtsam/archive/4.0.2.zip \
   && unzip gtsam.zip \
   && cd gtsam-4.0.2/ \
   && mkdir build && cd build \
   && cmake -DGTSAM_BUILD_WITH_MARCH_NATIVE=OFF .. \
   && make install -j4

# Creating ros_ws
RUN mkdir -p ~/ros_ws/src 
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && \
                  cd ~/ros_ws/ && \
                  catkin_make && \
                  echo 'source ~/ros_ws/devel/setup.bash' >> ~/.bashrc && \
                  echo 'source ~/ros_ws/devel/setup.bash' >> /root/.bashrc "

# copying bacchus repo
#ADD . /home/ubuntu/ros_ws/src/bacchus_lcas
RUN cd ~/ros_ws/src; git clone -b summer_school_2021 --recursive https://github.com/LCAS/bacchus_lcas.git

# Installing dependecies and compiling
RUN . /opt/ros/melodic/setup.sh; rosdep install --from-paths /home/ubuntu/ros_ws/src/bacchus_lcas/bacchus_gazebo  -y
RUN . /opt/ros/melodic/setup.sh; rosdep install --from-paths /home/ubuntu/ros_ws/src/bacchus_lcas/bacchus_move_base  -y
RUN . /opt/ros/melodic/setup.sh; rosdep install --from-paths /home/ubuntu/ros_ws/src/bacchus_lcas/bacchus_slam  -y
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /home/ubuntu/ros_ws; catkin_make'

RUN cd ~/ros_ws/src/bacchus_lcas/bacchus_slam; git submodule add -f https://github.com/osrf/gzweb; cd gzweb; git checkout gzweb_1.4.1

RUN bash -c "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash"
RUN bash -i -c "cat ~/.bashrc; source ~/.bashrc; source /home/ubuntu/ros_ws/devel/setup.bash; nvm install 8; cd /home/ubuntu/ros_ws/src/bacchus_lcas/bacchus_slam/gzweb; npm run deploy --- -m local"

# start gzweb server in /home/ubuntu/ros_ws/src/bacchus_lcas/bacchus_slam/gzweb with npm start 