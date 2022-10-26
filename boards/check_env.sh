#!/bin/bash

set -e

if [[ -z $(vitis -version | fgrep 2022.1) ]]; then
        echo "Error: Please source Vitis 2022.1 settings."
        exit 1
fi

if [[ -z ${XILINX_XRT} ]]; then
        echo "Error: Please source XRT 2021.1 settings."
        exit 1
fi
