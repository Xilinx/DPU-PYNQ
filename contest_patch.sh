#!/bin/bash

unzip vai3.5_kr260.zip

# won't have to do this once .deb packages are in opendownloads
echo "Installing VART packages"
pushd vai3.5_kr260/target/runtime_deb/
sudo bash setup.sh

# won't have to do this once these .so's are in opendownloads / we get an xrt_2.15.deb
cd ..
echo "Extracting prebuilt xrt libs..."
tar -xzf lack_lib.tar.gz
echo "Copying .so files to /usr/lib/"
sudo cp -r lack_lib/* /usr/lib

# thse will need to be available in opendownloads / installed with new xrt_2.15.deb
popd
echo "Copying pre-compiled xbutils to /usr/bin/unwrapped"
sudo cp xbutil2 /usr/bin/unwrapped/

echo "Patching /etc/profile.d/pynq_venv.sh"
sudo sed -i -e '$aexport LD_LIBRARY_PATH=/usr/lib' /etc/profile.d/pynq_venv.sh