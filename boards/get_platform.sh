#!/bin/bash

BOARD=$1
VITIS_PLATFORM=$2
PFM_NAME=$(echo $2 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
CURDIR=$(pwd)

if [ ! -d PYNQ-derivative-overlays ]; then
	git clone https://github.com/yunqu/PYNQ-derivative-overlays.git
	cd PYNQ-derivative-overlays
	git checkout -b temp tags/v2020.2
fi
cd ${CURDIR}/PYNQ-derivative-overlays/dpu
make clean && make BOARD=${BOARD}
cd ${CURDIR}/PYNQ-derivative-overlays/vitis_platform
make XSA_PATH=../dpu/dpu.xsa BOARD=${BOARD}
cp -rf ${CURDIR}/PYNQ-derivative-overlays/vitis_platform/${BOARD}/platforms/${PFM_NAME} ${CURDIR}/${BOARD}
cd ${CURDIR}

