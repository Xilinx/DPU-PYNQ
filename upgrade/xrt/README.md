# XRT upgrade

This subpackage will install XRT (tag: `2019.2_RC2`) onto your PYNQ image.
Although this is tested only on Ultra96v2 image, it should also work
on other Zynq Ultrascale boards, such as Ultra96v1, ZCU104, etc.

During the installation, the following things will happen:

1. The kernel source will be unpacked on your rootfs. 
2. The `zocl.ko` file will be rebuilt on your board; this new kernel driver 
will replace the old 2019.1 version.
3. The 2019.2 XRT software will be bootstrapped on your board.
