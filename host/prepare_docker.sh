#/bin/bash

#docker pull xilinx/vitis-ai-cpu:2.5

wget https://github.com/Xilinx/Vitis-AI/raw/v2.5/docker_run.sh
wget https://github.com/Xilinx/Vitis-AI/raw/v2.5/docker/dockerfiles/PROMPT.txt

sed -i 's/.\/docker\/dockerfiles\/PROMPT.txt/PROMPT.txt/g' docker_run.sh
chmod a+x docker_run.sh
