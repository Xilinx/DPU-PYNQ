#!/bin/bash

set -e
set -x

version=3.6.1
if [ ! -f protobuf-${version}.tar.gz ]; then
	wget -O protobuf-${version}.tar.gz \
		"https://www.xilinx.com/bin/public/openDownload?filename=protobuf-${version}.tar.gz"
fi
cp protobuf-${version}.tar.gz /root

cd /root
tar -xvf protobuf-${version}.tar.gz
cp -rf protobuf-dist/* /usr/local/
echo "/usr/local/lib" >> /etc/ld.so.conf.d/protobuf.conf
ldconfig

cd /root
rm -rf *.tar.gz protobuf-dist
