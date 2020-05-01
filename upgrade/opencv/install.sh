#!/bin/bash

set -e
set -x

version=3.4.3
if [ ! -f opencv-${version}.tar.gz ]; then
	wget -O opencv-${version}.tar.gz \
		"https://www.xilinx.com/bin/public/openDownload?filename=opencv-${version}.tar.gz"
fi
cp -rf opencv-${version}.tar.gz /root

cd /root
tar -xvf opencv-${version}.tar.gz
cp -rf opencv-dist/* /usr/local/
echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf
ldconfig

cd /root
rm -rf *.tar.gz opencv-dist
