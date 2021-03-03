#!/bin/bash

set -e
set -x

# patch xrt repo
CURDIR=$(pwd)
xrt_path=${CURDIR}/xrt-git

git clone https://github.com/xilinx/XRT.git xrt-git
cd xrt-git
git checkout -b temp tags/202020.2.8.726
cp -rf ../0001-Fix-flag-missing.patch .
git apply 0001-Fix-flag-missing.patch

# build kernel module
if [ ! -d ${xrt_path} ]; then
  echo "ERROR: Unable to locate XRT folder"
  exit 0
fi

cd /usr/src/kernel
sudo make modules_prepare
sudo make scripts
cd ${CURDIR}/xrt-git/src/runtime_src/core/edge/drm
make LINUXDIR=/lib/modules/5.4.0-xilinx-v2020.1/source CROSS_COMPILE=

# replace kernel module
if lsmod | grep "zocl" &> /dev/null ; then
	rmmod zocl
fi


if [ -f "/lib/modules/5.4.0-xilinx-v2020.1/extra/zocl.ko" ]; then
	mv -f /lib/modules/5.4.0-xilinx-v2020.1/extra/zocl.ko \
		/lib/modules/5.4.0-xilinx-v2020.1/extra/zocl.ko.2020.1
fi
sudo cp -f ${CURDIR}/xrt-git/src/runtime_src/core/edge/drm/zocl/zocl.ko \
		/lib/modules/5.4.0-xilinx-v2020.1/extra/zocl.ko
insmod /lib/modules/5.4.0-xilinx-v2020.1/extra/zocl.ko
if lsmod | grep "zocl" &> /dev/null ; then
	echo "Kernel driver zocl.ko has been successfully inserted."
else
	echo "Kernel driver zocl.ko is missing."
fi

cd ${CURDIR}/xrt-git/build
chmod 755 build.sh
XRT_NATIVE_BUILD=no ./build.sh -dbg
cd Debug
make install
