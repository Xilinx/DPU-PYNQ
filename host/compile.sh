#!/bin/bash

set -e

if [ "$#" -eq 2 ]; then
	BOARD=$1
	MODEL_NAME=$2
else
	echo "Error: please provide BOARD and MODEL_NAME as arguments."
	echo "Example: ./compile.sh Ultra96 cf_resnet50_imagenet_224_224_7.7G_1.4"
	exit 1
fi

if [ $BOARD = "Ultra96" ] && [ ! -e arch.json ]; then
	echo "Error: please make sure arch.json is in the working directory."
	exit 1
fi

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
elif [ $FRAMEWORK = 'tf2' ]; then
	conda activate vitis-ai-tensorflow2
elif [ $FRAMEWORK = 'pt' ]; then
	conda activate vitis-ai-pytorch
else
	echo "Error: please select a supported framework."
	echo "Currently supported: caffe, tensorflow, tensorflow2 and pytorch"
	exit 1
fi

# If custom Ultra96 json file is provided, add DPU support
if [ $BOARD = "Ultra96" ]; then
	sudo mkdir -p /opt/vitis_ai/compiler/arch/DPUCZDX8G/Ultra96
	sudo cp -f arch.json \
		/opt/vitis_ai/compiler/arch/DPUCZDX8G/Ultra96/arch.json
fi

mkdir -p ${BOARD}_${FRAMEWORK}_${MODEL}_build

# Download model if it doesn't already exist in workspace
if [ ! -f $MODEL_ZIP ]; then
	wget -O ${MODEL_ZIP} \
	"https://www.xilinx.com/bin/public/openDownload?filename=${MODEL_ZIP}"
fi

cp -f $MODEL_ZIP ${BOARD}_${FRAMEWORK}_${MODEL}_build/
cd ${BOARD}_${FRAMEWORK}_${MODEL}_build
unzip -o ${MODEL_ZIP}

# Compile the model
# pytorch model naming convention changes, so doing a wildflag
if [ $FRAMEWORK = 'cf' ]; then
	vai_c_caffe \
		--prototxt ${MODEL_UNZIP}/fix/deploy.prototxt \
		--caffemodel ${MODEL_UNZIP}/fix/deploy.caffemodel \
		--arch /opt/vitis_ai/compiler/arch/DPUCZDX8G/${BOARD}/arch.json \
		--output_dir . \
		--net_name ${MODEL}
elif [ $FRAMEWORK = 'tf' ]; then
	vai_c_tensorflow \
		--frozen_pb ${MODEL_UNZIP}/quantized/quantize_eval_model.pb \
		--arch /opt/vitis_ai/compiler/arch/DPUCZDX8G/${BOARD}/arch.json \
		--output_dir . \
		--net_name tf_${MODEL}
elif [ $FRAMEWORK = 'tf2' ]; then
	vai_c_tensorflow2 \
		--model ${MODEL_UNZIP}/quantized/quantized.h5 \
		--arch /opt/vitis_ai/compiler/arch/DPUCZDX8G/${BOARD}/arch.json \
		--output_dir . \
		--net_name tf2_${MODEL}
elif [ $FRAMEWORK = 'pt' ]; then
	vai_c_xir \
		--xmodel ${MODEL_UNZIP}/quantized/*.xmodel \
		--arch /opt/vitis_ai/compiler/arch/DPUCZDX8G/${BOARD}/arch.json \
		--output_dir . \
		--net_name pt_${MODEL}
else
	echo "Error: currently only caffe, tensorflow, tensorflow2 and pytorch are supported."
	exit 1
fi

rm -f ${MODEL_NAME}*zip
rm -rf ${MODEL_NAME}
cd ..
