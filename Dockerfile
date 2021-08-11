FROM lcasuol/vnc-server:latest

USER root:root

RUN apt-get update; apt-get upgrade -y \
    && apt-get purge -y ros-melodic-uol-cmp9767m-base \
#	&& apt-get install -y ros-melodic-bacchus-gazebo \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /home/lcas

RUN . /opt/ros/melodic/setup.sh; \
    cd /home/lcas \
    && mkdir -p workspace/bacchus_ws/src \
    && cd workspace/bacchus_ws/src \
    && catkin_init_workspace \
    && cd ..

# ADD  . /home/lcas/workspace/bacchus_ws/src/bacchus_lcas

RUN git clone --recursive -b summer_school_2021 https://github.com/LCAS/bacchus_lcas.git
RUN apt-get install -y ros-melodic-navigation ros-melodic-robot-localization ros-melodic-robot-state-publisher
RUN wget -O ~/Downloads/gtsam.zip https://github.com/borglab/gtsam/archive/4.0.2.zip \
    && cd ~/Downloads/ && unzip gtsam.zip -d ~/Downloads/ \
    && cd ~/Downloads/gtsam-4.0.2/ \
    && mkdir build && cd build \
    && cmake -DGTSAM_BUILD_WITH_MARCH_NATIVE=OFF .. \
    && sudo make install -j4

RUN apt-get update; . /opt/ros/melodic/setup.sh; rosdep install --from-paths /home/lcas/workspace/bacchus_ws/src -i -y
RUN ls -l /home/lcas/workspace/bacchus_ws; cd /home/lcas/workspace/bacchus_ws; . /opt/ros/melodic/setup.sh; catkin build
RUN chown -vR lcas:lcas /home/lcas/workspace

RUN echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
RUN echo "source /home/lcas/workspace/bacchus_ws/devel/setup.bash" >> ~/.bashrc

CMD bash -c "source /home/lcas/workspace/bacchus_ws/devel/setup.bash;  (/usr/local/lib/remote_manager/vnc_runner/noVNC/utils/launch.sh --vnc localhost:5901 --listen 6080 &);  rm -f /tmp/.X1-lock /tmp/.X11-unix/X1; vncserver -localhost yes -depth 24 -geometry 1920x1080 -SecurityTypes None -fg :1"

