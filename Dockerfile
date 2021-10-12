FROM tiryoh/ros-desktop-vnc:melodic

RUN apt-get update; apt-get -y upgrade

# Add repos
## LCAS
RUN curl https://raw.githubusercontent.com/LCAS/rosdistro/master/lcas-rosdistro-setup.sh | bash -
## Gazebo
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
RUN wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

RUN apt-get update; apt-get -y upgrade


# Creating ros_ws
RUN mkdir -p ~/ros_ws/src 
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && \
                  cd ~/ros_ws/ && \
                  catkin_make && \
                  echo 'source ~/ros_ws/devel/setup.bash' >> ~/.bashrc && \
                  echo 'source ~/ros_ws/devel/setup.bash' >> /root/.bashrc "

# copying bacchus repo
#ADD . /home/ubuntu/ros_ws/src/bacchus_lcas
RUN cd ~/ros_ws/src; git clone -b teaching --recursive https://github.com/LCAS/bacchus_lcas.git
RUN cd ~/ros_ws/src; git clone -b master --recursive https://github.com/LCAS/CMP9767M.git


# Installing dependecies and compiling
RUN . /opt/ros/melodic/setup.sh; rosdep install --from-paths /home/ubuntu/ros_ws/src/bacchus_lcas/bacchus_gazebo  -y
RUN . /opt/ros/melodic/setup.sh; rosdep install --from-paths /home/ubuntu/ros_ws/src/bacchus_lcas/bacchus_move_base  -y
RUN . /opt/ros/melodic/setup.sh; rosdep install --from-paths /home/ubuntu/ros_ws/src/CMP9767M  -y
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /home/ubuntu/ros_ws; catkin_make'
