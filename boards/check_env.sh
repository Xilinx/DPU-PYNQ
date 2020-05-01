#!/bin/bash

set -e

if [[ -z $(vitis -version | fgrep 2019.2) ]]; then
        echo "Error: Please source Vitis 2019.2 settings."
        exit 1
fi

if [[ -z ${XILINX_XRT} ]]; then
        echo "Error: Please source XRT 2019.2 settings."
        exit 1
fi
