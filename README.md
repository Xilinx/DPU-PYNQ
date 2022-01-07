# DPU on PYNQ

This repository holds the PYNQ DPU overlay. Specifically, the Vitis AI DPU 
is included in the accompanying bitstreams with example training and inference
notebooks ready to run on PYNQ enabled platforms.
Steps are also included to rebuild the designs in Vitis and can
be ported onto PYNQ-enabled Zynq Ultrascale+ boards.

In this repository, we currently support the following boards:

* Ultra96
* ZCU104
* KV260 (coming soon)

Other Zynq Ultrascale+ boards may be supported with few adjustments.
This repository supports Vitis AI 1.4.0.

## Quick Start

### 1. Install

To install the pynq-dpu on your board, simply run:

```shell
pip3 install pynq-dpu --no-build-isolation
```

Then go to your jupyter notebook home folder and fetch the notebooks:

```shell
cd $PYNQ_JUPYTER_NOTEBOOKS
pynq get-notebooks pynq-dpu -p .
```

This will make sure the desired notebooks shows up in your jupyter notebook 
folder.

### 2. Run

You are ready to go! Now in jupyter, you can explore the notebooks 
in `pynq-dpu` folder.

## Rebuild DPU Block Design

The DPU IP comes from the [Vitis Ai Github](https://github.com/Xilinx/Vitis-AI/tree/v1.4.0).
If you want to rebuild the hardware project, you can refer to the
[instructions for DPU Hardware Design](./boards/README.md).

In short, the following files will be generated in `boards/<Board>` folder:

1. `dpu.bit`
2. `dpu.hwh`
3. `dpu.xclbin`

These are the overlay files that can be used by the `pynq_dpu` package.

## Rebuild DPU Models

[DPU models](https://github.com/Xilinx/Vitis-AI/tree/v1.4) 
are available on the Vitis AI GitHub repository [model zoo](https://github.com/Xilinx/Vitis-AI/tree/v1.4/models/AI-Model-Zoo),
where you can find a model-list containing quantized models, as well as pre-compiled .xmodel files
that can be directly loaded into your DPU application.

If you want to recompile the DPU models or train your own network, you can refer to the
[instructions for DPU models](./host/README.md).


----
----

Copyright (C) 2021 Xilinx, Inc

SPDX-License-Identifier: Apache-2.0
