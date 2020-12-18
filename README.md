# DPU on PYNQ

This repository holds the PYNQ DPU overlay. Specifically, the Vitis AI DPU 
is included in the accompanying bitstreams with example training and inference
notebooks ready to run on PYNQ enabled platforms.
Steps are also included to rebuild the designs in Vitis and can
be ported onto PYNQ-enabled Zynq Ultrascale+ boards.

In this repository, we currently support the following boards:

* Ultra96
* ZCU104
* ZCU111

Other Zynq Ultrascale+ boards may be supported with few adjustments.
This repository supports Vitis AI 1.2.

## Quick Start

### 1. Upgrading the PYNQ v2.6 image

This upgrade step is to make sure users have a DPU-ready image. 
This step is only required for one time.

On your board, run `su` to use super user. Then run the following commands:

```shell
git clone --recursive --shallow-submodules https://github.com/Xilinx/DPU-PYNQ.git
cd DPU-PYNQ/upgrade
make
```

The upgrade process may take up to 1 hour, since a few packages will 
need to be installed. Please be patient. For more information, users can check
the [PYNQ v2.6 upgrade instructions](./upgrade/README.md)

### 2. Install

Run the following on board:

```shell
pip3 install pynq-dpu
```

Then go to your jupyter notebook home folder and fetch the notebooks:

```shell
cd $PYNQ_JUPYTER_NOTEBOOKS
pynq get-notebooks pynq-dpu -p .
```

This will make sure the desired notebooks shows up in your jupyter notebook 
folder.

### 3. Run

You are ready to go! Now in jupyter, you can explore the notebooks 
in `pynq-dpu` folder.

## Rebuild DPU Block Design

The DPU IP comes from the [Vitis Ai Github](https://github.com/Xilinx/Vitis-AI/tree/v1.2.1).
If you want to rebuild the hardware project, you can refer to the
[instructions for DPU Hardware Design](./boards/README.md).

In short, the following files will be generated in `boards/<Board>` folder:

1. `dpu.bit`
2. `dpu.hwh`
3. `dpu.xclbin`

These are the overlay files that can be used by the `pynq_dpu` package.

## Rebuild DPU Models

[DPU models for ZCU104](https://github.com/Xilinx/Vitis-AI/tree/v1.2.1) 
are available on the Vitis AI GitHub repository.

If you want to rebuild the DPU models, you can refer to the
[instructions for DPU models](./host/README.md).


Copyright (C) 2020 Xilinx, Inc
