# DPU Hardware Design

Make sure you have cloned this repository onto your host machine. We will
leverage the DPU IP officially released in the Vitis AI repository, so we
need to populate the submodule in DPU-PYNQ repository.

If you have not cloned the repo yet:

```bash
git clone --recursive --shallow-submodules https://github.com/Xilinx/DPU-PYNQ.git
cd DPU-PYNQ/boards
```

If you have already cloned the repository, make sure submodules are loaded:

```bash
cd DPU-PYNQ
git submodule init
git submodule update
```

## Officially Supported Boards

Currently we support the following boards:

* Ultra96
* ZCU104
* KV260

The DPU configurations for ZCU104 and KV260 are identical, however the vivado
designs can differ between boards. Some helpful examples for the KV260 can be
found on the KV260-Vitis [github repository](https://github.com/Xilinx/kv260-vitis/tree/release-2021.1).
And for the ZCU104 configurations exist on the Vitis AI repository [Vitis TRD flow](https://github.com/Xilinx/Vitis-AI/tree/v1.4/dsa/DPU-TRD/prj/Vitis)
The Ultra96 configuration is taken directly from the Avnet Vitis [github repository](https://github.com/Avnet/vitis/tree/2021.1/app/dpu/u96v2_sbc_base).

To build the DPU hardware design, we first need to make sure Vitis and XRT 
have been installed and their settings are sourced properly.

```shell
source <vitis-install-path>/Vitis/2021.1/settings64.sh
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

For more information regarding the DPU IP, you can refer to the [official Vitis
AI DPU guide](https://www.xilinx.com/html_docs/vitis_ai/1_4/fke1606771875742.html).

----
----

Copyright (C) 2021 Xilinx, Inc

SPDX-License-Identifier: Apache-2.0 License
