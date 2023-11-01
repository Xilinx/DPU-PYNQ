#!/bin/bash

set -e

if [[ -z $(vitis -version | fgrep 2023.1) ]]; then
        echo "Error: Please source Vitis 2023.1 settings."
        exit 1
fi

if [[ -z ${XILINX_XRT} ]]; then
        echo "Error: Please source XRT 2023.1 settings."
        exit 1
fi
