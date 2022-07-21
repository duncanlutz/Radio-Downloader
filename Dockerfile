FROM ubuntu:latest
ENV OPENCV_VERSION 4.6.0

RUN apt-get -y update && apt-get install -y gnupg2

RUN apt-key adv --refresh-keys --keyserver keyserver.ubuntu.com 

# Install all dependencies for OpenCV
RUN apt-get -y install \
    python3.10 \
    python3.10-dev \
    git \
    wget \
    unzip \
    cmake \
    build-essential \
    pkg-config \
    libatlas-base-dev \
    gfortran \
    libgtk2.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libv4l-dev \
    && \

    # install python dependencies
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py && \
    pip3 install numpy \
    && \

    # Install OpenCV
    wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip -O opencv3.zip && \
    unzip -q opencv3.zip && \
    mv /opencv-$OPENCV_VERSION /opencv && \
    rm opencv3.zip && \
    wget https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip -O opencv_contrib3.zip && \
    unzip -q opencv_contrib3.zip && \
    mv /opencv_contrib-$OPENCV_VERSION /opencv_contrib && \
    rm opencv_contrib3.zip \
    && \

    # Prepare build
    mkdir /opencv/build && cd /opencv/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D BUILD_PYTHON_SUPPORT=ON \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \
    -D BUILD_EXAMPLES=OFF \
    -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 \
    -D BUILD_opencv_python3=ON \
    -D BUILD_opencv_python2=OFF \
    -D WITH_IPP=OFF \
    -D WITH_FFMPEG=ON \
    -D WITH_V4L=ON .. \
    && \

    # Install
    cd /opencv/build && \
    make -j$(nproc) && \
    make install && \
    ldconfig

# Clean
RUN apt-get -y remove \
    python3-dev \
    libatlas-base-dev \
    gfortran \
    libgtk2.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libv4l-dev \
    && \
    apt-get clean && \
    rm -rf /opencv /opencv_contrib /var/lib/apt/lists/*

RUN apt update
RUN apt install -y ffmpeg

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

RUN echo 'TERM=xterm-256color' >> /etc/environment

WORKDIR /app
COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Define default command.
CMD ["python3", "download-function.py"]