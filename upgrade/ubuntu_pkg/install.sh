#!/bin/bash

set -e
set -x

apt-get autoremove -y libopencv* opencv-data python-opencv python3-opencv
apt-get update
apt-get install -y devmem2 at-spi2-core
apt-get install -y libgoogle-glog-dev libgoogle-glog0v5 
apt-get install -y libgflags-dev libgflags2.2
