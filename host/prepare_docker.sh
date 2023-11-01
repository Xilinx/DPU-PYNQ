#/bin/bash

mkdir -p docker/dockerfiles/PROMPT
wget https://github.com/Xilinx/Vitis-AI/raw/v3.5/docker_run.sh
wget -O docker/dockerfiles/PROMPT/PROMPT_cpu.txt https://github.com/Xilinx/Vitis-AI/raw/v3.5/docker/dockerfiles/PROMPT/PROMPT_cpu.txt
wget -O docker/dockerfiles/PROMPT/PROMPT_gpu.txt https://github.com/Xilinx/Vitis-AI/raw/v3.5/docker/dockerfiles/PROMPT/PROMPT_gpu.txt
wget -O docker/dockerfiles/PROMPT/PROMPT_rocm.txt https://github.com/Xilinx/Vitis-AI/raw/v3.5/docker/dockerfiles/PROMPT/PROMPT_rocm.txt
chmod a+x docker_run.sh
