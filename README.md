# DPU on PYNQ

This repository holds the PYNQ DPU overlay. Specifically, the Vitis AI DPU is included in the accompanying bitstreams with example training and inference notebooks ready to run on PYNQ enabled platforms. Steps are also included to rebuild the designs in Vitis and can be ported onto PYNQ-enabled Zynq Ultrascale+ boards. 

This release of DPU-PYNQ supports PYNQ 3.0 and Vitis AI 2.5.0.

## Board Support

DPU-PYNQ is available for a wide range of boards and devices, some of which may not have official PYNQ images available, however the platforms and overlays can still be used in a variety of custom accelerator applications.

| Platform  | DPU Architecture  | Number of cores  | Verified  |
|---        |:---:              |:---:             |:---:      |
| KR260 SOM       | B4096  | 1  | Yes  |
| KV260 SOM       | B4096  | 1  | Yes  |
| Pynq-ZU         | B4096  | 1  | Yes  |
| RFSoC2x2        | B4096  | 2  | Yes  |
| RFSoC4x2        | B4096  | 2  | Yes  |
| Ultra96v2       | B1600  | 1  | Yes  |
| ZCU104          | B4096  | 2  | Yes  |
| ZCU111          | B4096  | 2  | Yes  |
| ZCU208          | B4096  | 2  | Yes  |
| Genesys ZU-5EV  | B4096  | 1  |   |
| T1 Telco RFSoC  | B4096  | 2  |   |
| T1 Telco MPSoc  | B4096  | 2  |   |
| TySOM-3A-ZU19EG | B4096  | 2  |   |
| TySOM-3-ZU7EV   | B4096  | 2  |   |
| Ultra96v1       | B1600  | 1  |   |
| UltraZed-EG     | B4096  | 1  |   |
| ZCU102          | B4096  | 2  |   |
| ZCU106          | B4096  | 2  |   |
| ZCU1285         | B4096  | 2  |   |
| ZCU216          | B4096  | 2  |   |
| ZUBoard-1CG     | B800   | 1  |   |

DPU overlays for most boards have been built using the B4096 architecture with 1 or 2 cores, compatible with the KV260/ZCU102/ZCU104 models in the Vitis AI Model Zoo. For a selection of smaller boards, like the Ultra96 and ZUBoard-1CG custom arch.json files are provided that will allow you to compile .xmodel files for those boards.

## Quick Start

### 1. Install

To install pynq-dpu on your PYNQ-enabled board, in the Jupyter Lab terminal, simply run:

```shell
pip3 install pynq-dpu --no-build-isolation
```

Then go to your jupyter notebook home folder and fetch the notebooks:

```shell
cd $PYNQ_JUPYTER_NOTEBOOKS
pynq get-notebooks pynq-dpu -p .
```

This will make sure the desired notebooks show up in your jupyter notebook 
folder.

### 1.b [Optional] Install from ssh/serial

If you are installing the package from an ssh or serial terminal instead of Jupyter Lab (e.g. using the usb network connection on the Ultra96 -- `ssh xilinx@192.168.3.1`).

Make sure you login as `root` (e.g., `sudo su`) and source the pynq profile scripts before installing the pynq_dpu package.

```shell
. /etc/profile.d/xrt_setup.sh
. /etc/profile.d/pynq_venv.sh
pip3 install pynq-dpu --no-build-isolation
```

### 2. Run

You are ready to go! Now in jupyter, you can explore the notebooks 
in the `pynq-dpu` folder.

## Selftest and Contributing

If you have a board that hasn't been marked as verified in the above table, you can use the new built-in tests to verify if DPU-PYNQ works on your device as intended. To verify that your installation was successful, without opening any notebooks you can run the tests that are part of the pynq_dpu package. Simply run:

```shell
python3 -m pytest --pyargs pynq_dpu
```

If the tests are successful please feel free to make a contribution to the above table by opening an pull request and updating the markdown entry for that board.

## Rebuild DPU Block Design

The DPU IP comes from the [Vitis Ai Github](https://github.com/Xilinx/Vitis-AI/tree/v2.5).
If you want to rebuild the hardware project, you can refer to the
[instructions for the DPU Hardware Design](./boards/README.md).

In short, the following files will be generated in `boards/<Board>` folder:

1. `dpu.bit`
2. `dpu.hwh`
3. `dpu.xclbin`

These are the overlay files that can be used by the `pynq_dpu` package.

## Rebuild DPU Models

[DPU models](https://github.com/Xilinx/Vitis-AI/tree/v2.5) 
are available on the Vitis AI GitHub repository [model zoo](https://github.com/Xilinx/Vitis-AI/tree/v2.5/model_zoo),
where you can find a model-list containing quantized models, as well as pre-compiled .xmodel files
that can be directly loaded into your DPU application.

If you want to recompile the DPU models or train your own network, you can refer to the
[instructions for DPU models](./host/README.md).


----
----

Copyright (C) 2021 Xilinx, Inc

SPDX-License-Identifier: Apache-2.0
