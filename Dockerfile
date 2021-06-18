FROM lcasuol/vnc-server:latest

# RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/packages.microsoft.gpg \
#         && install -o root -g root -m 644 /tmp/packages.microsoft.gpg /etc/apt/trusted.gpg.d/ \
#         && sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'

# # ensure busting the cache
# ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

# RUN apt-get update || true
# RUN apt-get upgrade -y \
# 	&& apt-get install -y xfce4-session xfce4-terminal xfce4-panel tigervnc-standalone-server dnsutils openssh-client mesa-utils firefox code \
# 		ros-melodic-uol-cmp9767m-tutorial ros-melodic-desktop python-catkin-tools ros-melodic-rqt-tf-tree \
# 		ros-melodic-opencv-apps ros-melodic-rqt-image-view ros-melodic-uol-cmp9767m-base ros-melodic-find-object-2d ros-melodic-video-stream-opencv ros-melodic-topic-tools \
# 		ros-melodic-rqt-tf-tree ros-melodic-find-object-2d ros-melodic-video-stream-opencv \
# 		ros-melodic-robot-localization ros-melodic-topological-navigation ros-melodic-amcl \
# 		ros-melodic-fake-localization ros-melodic-carrot-planner ros-melodic-gmapping \
# 		ros-melodic-uol-cmp3103m git tmux net-tools \
# 	&& apt-get clean \
# 	&& rm -rf /var/lib/apt/lists/*

# RUN mkdir -p /usr/local/lib && git -C /usr/local/lib clone --recursive https://github.com/marc-hanheide/remote_manager.git && git clone https://github.com/novnc/websockify /usr/local/lib/remote_manager/vnc_runner/noVNC/utils/websockify
# RUN mkdir -p /usr/local/bin && install /usr/local/lib/remote_manager/network-scripts/bin/ngrok1.lnx /usr/local/bin/ngrok1

# RUN groupadd -g 2000 lcas && useradd -u 2000 -m -s /bin/bash -g lcas -G sudo -p '$6$w7.YBFojp1W3dXFX$gH4r7JkBEMhWjO4sn5arV8EuLIS7NKPYAOrLPXWdJILlYowJQbs3K2ZogmnRgh/DyyaSVxtDDty8rbf.17rQa.' lcas

# RUN mkdir -p /home/lcas/.config/rosdistro/
# RUN echo "index_url: https://raw.github.com/lcas/rosdistro/master/index.yaml" > /home/lcas/.config/rosdistro/index.yaml
# RUN echo "index_url: https://raw.github.com/lcas/rosdistro/master/index-v4.yaml" > /home/lcas/.config/rosdistro/index-v4.yaml
# RUN bash -c "source /opt/ros/melodic/setup.bash;\
# 	export ROSDISTRO_INDEX_URL=https://raw.github.com/lcas/rosdistro/master/index-v4.yaml; \
#         rosdep update"
# RUN chown -R 2000:2000 /home/lcas

# ENV ROSDISTRO_INDEX_URL https://raw.github.com/lcas/rosdistro/master/index-v4.yaml

# VOLUME /home/lcas

# EXPOSE 6080 

# USER lcas:lcas
# WORKDIR /home/lcas

USER root:root

RUN apt-get update; apt-get upgrade -y \
    && apt-get purge -y ros-melodic-uol-cmp9767m-base \
	&& apt-get install -y ros-melodic-bacchus-gazebo \
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
ADD  . /home/lcas/workspace/bacchus_ws/src/bacchus_lcas
RUN apt-get update; . /opt/ros/melodic/setup.sh; rosdep install --from-paths /home/lcas/workspace/bacchus_ws/src -i -y
RUN ls -l /home/lcas/workspace/bacchus_ws; cd /home/lcas/workspace/bacchus_ws; . /opt/ros/melodic/setup.sh; catkin build
RUN chown -vR lcas:lcas /home/lcas/workspace

CMD bash -c "source /home/lcas/workspace/bacchus_ws/devel/setup.bash;  (/usr/local/lib/remote_manager/vnc_runner/noVNC/utils/launch.sh --vnc localhost:5901 --listen 6080 &);  rm -f /tmp/.X1-lock /tmp/.X11-unix/X1; vncserver -localhost yes -depth 24 -geometry 1280x720 -SecurityTypes None -fg :1"

