#!/bin/bash

set -e
set -x

version=0.4.0
wget "https://github.com/google/glog/archive/v${version}.zip"
unzip v${version}.zip
cd glog-${version}
mkdir -p build
cd build
cmake -DBUILD_SHARED_LIBS=on \
	-DCMAKE_INSTALL_PREFIX=/usr/local \
	-DCMAKE_BUILD_TYPE=Release \
	..
make -j
make install
echo "/usr/local/lib" >> /etc/ld.so.conf.d/glog.conf
ldconfig

cd /root
rm -rf glog-${version} *.zip
