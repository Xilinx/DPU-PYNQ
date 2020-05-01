#!/bin/bash

if [ $(id -u) != "0" ]; then
	echo "Error: install scripts require root or sudo."
	exit 1
fi

if [ $(arch) != 'aarch64' ]; then
	echo "Error: only Zynq Ultrascale boards are supported."
	exit 1
fi

if [ $(df -h -BG | grep /dev/root | \
		awk '{print $2}' | sed 's/G//g') -lt 10 ]; then
	echo "Error: not enough disk space; recommend to use >16GB SD card."
	exit 1
fi

url="https://www.xilinx.com"
wget -qO- $url &> /dev/null
if [ $? -ne 0 ]; then
	echo "Error: please make sure you have valid Internet connection."
	exit 1
fi
