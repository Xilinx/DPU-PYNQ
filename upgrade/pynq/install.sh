#!/bin/bash

set -e
set -x

# check version
cur_version=$(python3 -c "import pynq;print(pynq.__version__)")
req_version="2.5.1"

# install pynq if it is not 2.5.1
if [[ ${cur_version} != ${req_version} ]]; then
	sudo pip3 uninstall -y pynq
	sudo pip3 install --upgrade --upgrade-strategy only-if-needed \
		pynq==${req_version}
fi

# remove backup notebook folder
rm -rf /home/xilinx/jupyter_notebooks_*
