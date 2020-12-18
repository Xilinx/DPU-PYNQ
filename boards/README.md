# DPU Hardware Design

Make sure you have cloned this repository onto your host machine:

```
git clone --recursive --shallow-submodules https://github.com/Xilinx/DPU-PYNQ.git
cd DPU-PYNQ/boards
```

## Officially Supported Boards

Currently we support the following boards:

* Ultra96
* ZCU104
* ZCU111

To build the DPU hardware design, we first need to make sure Vitis and XRT 
have been installed and their settings are sourced properly.

```shell
source <vitis-install-path>/Vitis/2020.1/settings64.sh
source <xrt-install-path>/xilinx/xrt/setup.sh
```

Then build the hardware design.

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
`dpu_conf.vh` and `prj_config` in that folder. 
After sourcing Vitis and XRT settings, you can run:

```shell
make BOARD=<Board> VITIS_PLATFORM=<Platform-location>
```

In general, to prepare the Vitis platform, users have the following options:

* Rebuild Vitis platform from source
(e.g. [source for Xilinx official platforms](https://github.com/Xilinx/Vitis_Embedded_Platform_Source/tree/master/Xilinx_Official_Platforms))
* Download an official Vitis platform
(e.g. [ZCU104 `platform`](https://www.xilinx.com/bin/public/openDownload?filename=zcu104_dpu_2020.1.zip))
* Provide users' own customized platforms

No matter how you have prepared your Vitis platform, you can always provide
`VITIS_PLATFORM` to the make process as shown above.

## DPU IP

You can modify the `dpu_conf.vh` file to change the DPU IP settings in the 
board folder. The adjustable settings of the DPU IP include: 

* DPU model number 
* `RAM_USAGE_LOW`
* `CHANNEL_AUGMENTATION_ENABLE`
* `DWCV_ENABLE`
* `POOL_AVG_ENABLE`
* `RELU_LEAKYRELU_RELU6`
* `Softmax`

For more information regarding the DPU IP, you can refer to the [official Vitis
AI DPU guide](https://github.com/Xilinx/Vitis-AI/blob/master/DPU-TRD/prj/Vitis/README.md).

Copyright (C) 2020 Xilinx, Inc
