# DPU Hardware Design

Make sure you have cloned this repository onto your host machine. To build the DPU overlays we will
leverage the DPU IP from the official Vitis AI [DPUCZDX8G TRD flow](https://docs.xilinx.com/r/en-US/pg338-dpu).

## Rebuilding Designs

To build the DPU hardware design, we first need to make sure Vitis and XRT 
have been installed and their settings are sourced properly.

```shell
source <vitis-install-path>/Vitis/2023.1/settings64.sh
source <xrt-install-path>/xilinx/xrt/setup.sh
```

Note that most boards in this repository grab board files from the XilinxBoardStore. Some community boards might get the board files from a different source. Make sure this is cloned into the DPU-PYNQ/boards folder before building any of the designs.

```shell
git clone https://github.com/Xilinx/XilinxBoardStore -b 2023.1
```

Then build the hardware design. Please note that in this case the `BOARD` variable should match the folder names in the DPU-PYNQ/boards directory.

```shell
make BOARD=<Board>
```

During this process, the corresponding Vitis platform will be generated
for the specified board. The make process generates in `<Board>`:

1. `dpu.bit`
2. `dpu.hwh`
3. `dpu.xclbin`

## Other Zynq Ultrascale Boards

You can create your own folder for your board; make sure you have 
`dpu_conf.vh` and `prj_config` in that folder, and a platform file 
`platform.xsa` or alternatively `gen_platform.tcl` script that would
generate a platform with that name. 
After sourcing Vitis and XRT settings, you can run:

```shell
make BOARD=<Board> VITIS_PLATFORM=<Platform-location>
```

In general, to prepare the Vitis platform, users have the following options:

* Rebuild Vitis platform from source
(e.g. [source for Xilinx official platforms](https://github.com/Xilinx/Vitis_Embedded_Platform_Source/tree/master/Xilinx_Official_Platforms))
* Download an official Vitis platform
* Provide users' own customized platforms

No matter how you have prepared your Vitis platform, you can always provide
`VITIS_PLATFORM` to the make process as shown above.

## DPU IP

You can modify the `dpu_conf.vh` file to change the DPU IP settings in the 
board folder. The adjustable settings of the DPU IP include: 

* `DPU model number` 
* `URAM_ENABLE`
* `RAM_USAGE_LOW`
* `CHANNEL_AUGMENTATION_ENABLE`
* `DWCV_ENABLE`
* `POOL_AVG_ENABLE`
* `RELU_LEAKYRELU_RELU6`
* `DSP48_USAGE_HIGH`
* `LOWPOWER_ENABLE`
* `DEVICE Configuration`

For more information regarding the DPU IP, you can refer to the official [Vitis
AI DPU IP guide](https://docs.xilinx.com/r/en-US/pg338-dpu).

----
----

Copyright (C) 2021 Xilinx, Inc

SPDX-License-Identifier: Apache-2.0 License
