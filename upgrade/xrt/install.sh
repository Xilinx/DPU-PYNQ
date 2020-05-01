#!/bin/bash

set -e
set -x

# patch xrt repo
CURDIR=$(pwd)
git clone https://github.com/Xilinx/XRT.git xrt-git
cd xrt-git
git checkout -b temp tags/2019.2_RC2
cp -rf ../0001-fix-for-pynq.patch .
git apply 0001-fix-for-pynq.patch

# build kernel module
cd /
sudo tar xvzf kernel.tgz
cd /usr/src/kernel
sudo make modules_prepare
sudo make scripts
cd ${CURDIR}/xrt-git/src/runtime_src/core/edge/drm
make LINUXDIR=/lib/modules/4.19.0-xilinx-v2019.1/source

# replace kernel module
if lsmod | grep "zocl" &> /dev/null ; then
	rmmod zocl
fi
mv -f /lib/modules/4.19.0-xilinx-v2019.1/extra/zocl.ko \
	/lib/modules/4.19.0-xilinx-v2019.1/extra/zocl.ko.2019.1
sudo cp -f ${CURDIR}/xrt-git/src/runtime_src/core/edge/drm/zocl/zocl.ko \
	/lib/modules/4.19.0-xilinx-v2019.1/extra/zocl.ko
insmod /lib/modules/4.19.0-xilinx-v2019.1/extra/zocl.ko
if lsmod | grep "zocl" &> /dev/null ; then
	echo "Kernel driver zocl.ko has been successfully inserted."
else
	echo "Kernel driver zocl.ko is missing."
fi

# build and install (dbg mode)
cd ${CURDIR}/xrt-git
cd build
chmod 755 build.sh
./build.sh -dbg
