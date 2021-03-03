# Build Machine Learning Models for DPU

This folder helps users recompile their own DPU models so they can be deployed
on the board. The recompilation is needed if users want to retarget
a different DPU configuration.

We provide a `compile.sh` script that helps users compile their own deployable
models from Vitis AI model zoo. 

## Prerequisites


### 1. Repository

Make sure you have cloned this repository onto your host machine:

```shell
git clone --recursive --shallow-submodules https://github.com/Xilinx/DPU-PYNQ.git
```

### 2. Docker

If you have not installed docker on your host machine, please refer to the
[Vitis AI getting started page](https://github.com/Xilinx/Vitis-AI/tree/v1.3#Getting-Started)
to install docker. 

### 3. (optional) `arch.json`

There are 3 cases for different boards:

1. For ZCU104, our DPU configuration is consistent with the ZCU104 design of
the Vitis AI release.
2. For ZCU111, our DPU configuration is consistent with the ZCU102 design of
the Vitis AI release.
3. For Ultra96 or other boards, the Vitis AI release does not contain
necessary files to recompile the DPU models directly.

For case 1 and 2, users can leverage existing files on the released docker 
image. No action is required.

For case 3 (Ultra96 or any other board), the proper DPU configuration file 
(`arch.json`) does not exist on the released docker image.
The compilation flow assumes the existence of this file and
copies it over to the docker environment.
We need to prepare `arch.json` if it does not exist.

If you have rebuilt the DPU hardware design by yourself, you can see
`arch.json` file inside folder 
`DPU-PYNQ/Boards/<Board>/binary_container_1/link/vivado/vpl/prj/prj.gen/sources_1/bd/dpu/ip/dpu_DPUCZDX8G_1_0/`.
You can also use the `find -name` command to locate this file.

For example, our `arch.json` file for Ultra96 DPU configuration has content:

```shell
{"fingerprint":"0x1000020f2014404"}
```

**Note**: if you have changed the DPU configurations in your hardware design, 
you must prepare your new `arch.json`.

### 4. (optional) Docker

If you want to run the jupyter notebook `train_mnist_model.ipynb` on the host
machine, you will need to make sure you have an AVX2 and FMA compatible 
machine. To check that:

```shell
grep avx2 /proc/cpuinfo
grep fma /proc/cpuinfo
```

Both commands should return a list of available supported instruction sets.
If one of the 2 commands returns nothing, your machine will have difficulties
importing `tensorflow` package.

Also, on the docker image, you need to do the following before running any Jupyter
notebook.

```shell
conda activate vitis-ai-tensorflow
yes | pip install matplotlib keras==2.2.5
```


## Build DPU Models from Vitis AI Model Zoo

On your host machine, as mentioned in the previous section, if you are
building models for Ultra96, you need to put the corresponding `arch.json`
file in folder `DPU-PYNQ/host`.

We can run the following commands now.

```shell
cd DPU-PYNQ/host
mkdir -p docker
cp -rf ../vitis-ai-git/docker_run.sh .
cp -rf ../vitis-ai-git/docker/PROMPT.txt docker
chmod u+x docker_run.sh
./docker_run.sh xilinx/vitis-ai-cpu:1.3.411
```

For the GPU accelerated docker image:
```
./docker_run.sh xilinx/vitis-ai:1.3.411
```

The `docker_run.sh` will download a Vitis AI docker image after users accept
the license agreements. It may take a long time to download since the image 
is about 8GB. After the download is complete, the `docker_run.sh` script 
will help you log onto that docker image.

The Vitis AI docker image gives users access to the Vitis AI utilities 
and compilation tools. If you have run `docker_run.sh` before, it will simply 
launch the docker image without downloading again. 

Once you are in the docker environment, you can run the `compile.sh` script.

```shell
./compile.sh <Board> <model_name>
```

Here `Board` can be `Ultra96`, `ZCU104`, and `ZCU111`. 

For `model_name ` and `model_performance`, 
users can check the [model performance](https://github.com/Xilinx/Vitis-AI/tree/v1.3/models/AI-Model-Zoo#Model-Performance) page as shown below.

![](images/model_info.png)

The `compile.sh` eases the compilation of existing DPU models. Users can also
adjust the script to compile their own models. The `compile.sh` does the
following things.

### (1) Adding Ultra96 support

We copy over the `arch.json` file.

### (2) Downloading a model from model zoo

We download a deployable model as a zip file from
[Vitis AI Model Zoo](https://github.com/Xilinx/Vitis-AI/tree/v1.3/models/AI-Model-Zoo#Model-Download).
The contents of the extracted zip file (e.g., `cf_resnet50_imagenet_224_224_7.7G`) 
will contain multiple versions of the model:

* floating point frozen graph (under `float`)
* quantized evaluation model (under `quantized`)
* quantized deployment model (under `quantized`)

In our case we only need the following files inside the `quantized` directory:
(1) `deploy.caffemodel` and (2) `deploy.prototxt`.

### (3) Compiling the model

We will compile the model into a `*.xmodel` file.
If everything is successful, you should see a screen as shown below.

![](images/vai_c_output_caffe.png)

A new model file (e.g. `dpu_resnet50_0.xmodel`) should appear in your `build/`
directory; this is the model file that can be deployed on the board.

After you are done with the docker environment, type in:

```shell
exit
```

to exit.

## Train Your Own DPU Models from Scratch

Instead of using the deployable models from the Vitis AI model zoo, advanced
users may even train their own machine learning models. We will show
one example in `train_mnist_model.ipynb`. 

Once you are in the docker environment, if you have not done the following, 
make sure you do it before running the notebook:

```shell
conda activate vitis-ai-tensorflow
yes | pip install matplotlib keras==2.2.5
```

Then launch jupyter notebook and run the `train_mnist_model.ipynb` 
step-by-step.

```shell
jupyter notebook --ip=0.0.0.0 --port=8080
```

For more information such as training your own model, please refer to the 
[Vitis AI user guide](https://www.xilinx.com/support/documentation/sw_manuals/vitis_ai/1_3/ug1414-vitis-ai.pdf)
and [Vitis AI Tutorials](https://github.com/xilinx/vitis-ai-tutorials).

## References

* [Vitis AI Github](https://github.com/Xilinx/Vitis-AI)
* [Vitis AI User Guide](https://www.xilinx.com/support/documentation/sw_manuals/vitis_ai/1_1/ug1414-vitis-ai.pdf)
* [Vitis AI Model Zoo](https://github.com/Xilinx/Vitis-AI/tree/v1.3/models/AI-Model-Zoo)

Copyright (C) 2021 Xilinx, Inc

SPDX-License-Identifier: Apache-2.0 License
