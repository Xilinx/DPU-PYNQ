#!/bin/bash

set -e

if [ "$#" -eq 2 ]; then
	BOARD=$1
	MODEL_NAME=$2
else
	echo "Error: please provide BOARD and MODEL_NAME as arguments."
	echo "Example: ./compile.sh Ultra96 cf_resnet50_imagenet_224_224_7.7G_1.1"
	exit 1
fi

if [ $BOARD = "Ultra96" ] && [ ! -e dpu.hwh ]; then
	echo "Error: please make sure dpu.hwh is in the working directory."
	exit 1
fi

VAI_VERSION=1.2
MODEL_ZIP=${MODEL_NAME}.zip
MODEL_UNZIP=$MODEL_NAME
MODEL=$(echo $MODEL_NAME | cut -d'_' -f2)
FRAMEWORK=$(echo $MODEL_NAME | cut -d'_' -f1)

# Activate Vtisi AI conda environment
source /etc/profile.d/conda.sh
if [ $FRAMEWORK = 'cf' ]; then
	conda activate vitis-ai-caffe
elif [ $FRAMEWORK = 'tf' ]; then
	conda activate vitis-ai-tensorflow
else
	echo "Error: currently only caffe and tensorflow are supported."
	exit 1
fi

# If custom Ultra96 hwh file is provided, add DPU support
if [ $BOARD = "Ultra96" ]; then
	sudo mkdir -p /opt/vitis_ai/compiler/arch/DPUCZDX8G/Ultra96
	sudo cp -f Ultra96.json \
		/opt/vitis_ai/compiler/arch/DPUCZDX8G/Ultra96/Ultra96.json
	dlet -f dpu.hwh
	sudo mv *.dcf /opt/vitis_ai/compiler/arch/DPUCZDX8G/${BOARD}/${BOARD}.dcf
fi

# ZCU111 and ZCU102 use equivalent DPU configurations
if [ $BOARD = "ZCU111" ]; then
	BOARD=ZCU102
fi

mkdir -p build
cd build

# Download model if it doesn't already exist in workspace
if [ ! -f $MODEL_ZIP ]; then
	wget -O ${MODEL_ZIP} \
	"https://www.xilinx.com/bin/public/openDownload?filename=${MODEL_ZIP}"
fi
unzip -o ${MODEL_ZIP}

# Compile the model
if [ $FRAMEWORK = 'cf' ]; then
	vai_c_caffe \
		--prototxt ${MODEL_UNZIP}/quantized/deploy.prototxt \
		--caffemodel ${MODEL_UNZIP}/quantized/deploy.caffemodel \
		--arch /opt/vitis_ai/compiler/arch/DPUCZDX8G/${BOARD}/${BOARD}.json \
		--output_dir . \
		--net_name ${MODEL}
elif [ $FRAMEWORK = 'tf' ]; then
	vai_c_tensorflow \
		--frozen_pb ${MODEL_UNZIP}/quantized/deploy_model.pb \
		--arch /opt/vitis_ai/compiler/arch/DPUCZDX8G/${BOARD}/${BOARD}.json \
		--output_dir . \
		--net_name tf_${MODEL}
else
	echo "Error: currently only caffe and tensorflow are supported."
	exit 1
fi

cd ..
