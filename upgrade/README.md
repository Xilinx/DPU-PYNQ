# DPU on PYNQ v2.5 Image

This folder helps users upgrade PYNQ v2.5 image to be 
compatible with Vitis AI. Currenly we support Zynq Ultrascale board images,
including Ultra96, ZCU104, ZCU111, and potentially a couple of other boards.

## Prerequisite

We have the following assumptions:

1. As a starting point, we assume you have flashed your SD card (at least
16GB) with PYNQ image v2.5.
2. You can boot up the board without any issue. For Ultra96, we recommended 
you to use bigger power bricks; for example, [4A power brick](https://www.avnet.com/shop/us/products/avid-technologies/90152-2208-3074457345635740760/).
3. You have an Internet connection from the board. Wired connection is 
recommended.

## Upgrade PYNQ Image

The first step is to upgrade your image so we can install some libraries 
required by Vitis AI. 

**On your board**, run `su` to use super
user. Password is `xilinx`. Run the following commands:

```shell
git clone --recursive --shallow-submodules https://github.com/Xilinx/DPU-PYNQ.git
cd DPU-PYNQ/upgrade
make
```

The upgrade process can take up to 1 hour so please be patient. 
At the same time, you can proceed to the next few steps.

By default, the `Makefile` will install / update the following packages:

* `pynq`: Install `pynq` 2.5.1 from source distribution.
* `xrt`: Xilinx Run Time (XRT) will be upgraded to tag `2019.2_RC2`.
* `ubuntu_pkg`: Install a couple of packages from Ubuntu repository; remove the old `opencv` package.
* `opencv`: Install `opencv` 3.4.3.
* `protobuf`: Install `protobuf` 3.6.1.
* `jsonc`: Install `json-c` 0.13.1.
* `dpu_clk`: Install a small Python script to control DPU clocks.
* `glog`: Install `glog` 0.4.0.

## Notes

The above steps help users with DPU on PYNQ image v2.5 temporarily. 
For future PYNQ releases, these steps will be included in the image itself, 
so we expect the upgrade scripts to be deprecated in the near future.

Copyright (C) 2020 Xilinx, Inc
