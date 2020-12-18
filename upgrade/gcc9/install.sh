#!/bin/bash

set -e
set -x

target="lsb-release"

sudo mv /etc/${target} /etc/${target}.tmp
sudo cp ./${target} /etc/.

sudo apt install software-properties-common
sudo add-apt-repository ppa:ubuntu-toolchain-r/test

sudo apt install gcc-9 g++-9

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 --slave /usr/bin/g++ g++ /usr/bin/g++-9 --slave /usr/bin/gcov gcov /usr/bin/gcov-9

sudo rm /etc/${target}
sudo mv /etc/${target}.tmp /etc/${target}

