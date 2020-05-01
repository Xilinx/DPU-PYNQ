#  Copyright (C) 2020 Xilinx, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import os
import subprocess
import pynq
from pynq import Register


__author__ = "Yun Rock Qu"
__copyright__ = "Copyright 2020, Xilinx"
__email__ = "pynq_support@xilinx.com"


DATA_WIDTH_REGISTER = 0xFF419000
MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
OVERLAY_PATH = os.path.join(MODULE_PATH, 'overlays')
XCL_DST_PATH = "/usr/lib"


def set_data_width(width_option):
    """Set AXI port data width.

    We need to select the 32/64/128-bit data width for the slave registers.
    Each of the following values corresponds to a specific data width.
    The reason why we need this step, is that for some petalinux BSP's
    (e.g. `xilinx-zcu104-v2019.1-final.bsp`), the AXI lite interface width
    is not set properly. This step may not be needed for future PYNQ
    releases.

    00: 32-bit AXI data width (default)
    01: 64-bit AXI data width
    10: 128-bit AXI data width (reset value)
    11: reserved

    Parameters
    ----------
    width_option : int
        The width options ranging from 0 to 3.

    """
    if width_option not in range(4):
        raise ValueError("Data width option can only be set to 0, 1, 2, 3.")
    Register(0xFF419000)[9:8] = width_option


def get_kernel_name_from_elf(model):
    """Parse the kernel name out of the given elf file.

    This method will take elf file as input, read its information, and
    return the model name.

    Parameters
    ----------
    model : str
        The name of the ML model binary. Can be absolute or relative path.

    """
    cmd = 'readelf {} -s | grep ' \
        '"1: 0000000000000000     0 FILE    LOCAL  DEFAULT  ABS"'.format(model)
    line = subprocess.check_output(cmd, shell=True).decode()
    kernel_0 = line.split()[-1].lstrip("dpu_").rstrip(".s")
    return kernel_0[:-len('_0')] if kernel_0.endswith('_0') else kernel_0


class DpuOverlay(pynq.Overlay):
    """DPU overlay class.

    This class inherits from the PYNQ overlay class. The initialization method
    is similar except that we have additional bit file search path.

    """
    def __init__(self, bitfile_name, dtbo=None,
                 download=True, ignore_version=False, device=None):
        """Initialization method.

        Check PYNQ overlay class for more information on parameters.

        By default, the bit file will be searched in the following paths:
        (1) the `overlays` folder inside this module; (2) an absolute path;
        (3) the relative path of the current working directory.

        """
        if os.path.isfile(bitfile_name):
            abs_bitfile_name = bitfile_name
        elif os.path.isfile(os.path.join(OVERLAY_PATH, bitfile_name)):
            abs_bitfile_name = os.path.join(OVERLAY_PATH, bitfile_name)
        else:
            raise FileNotFoundError('Cannot find {}.'.format(bitfile_name))
        super().__init__(abs_bitfile_name,
                         dtbo=dtbo,
                         download=download,
                         ignore_version=ignore_version,
                         device=device)
        self.overlay_dirname = os.path.dirname(self.bitfile_name)
        self.overlay_basename = os.path.basename(self.bitfile_name)

    def download(self):
        """Download the overlay.

        This method overwrites the existing `download()` method defined in
        the overlay class. It will download the bitstream, set AXI data width,
        copy xclbin and ML model files.

        """
        super().download()
        self.overlay_dirname = os.path.dirname(self.bitfile_name)
        self.overlay_basename = os.path.basename(self.bitfile_name)

        set_data_width(0)
        self.copy_xclbin()

    def copy_xclbin(self):
        """Copy the xclbin file to a specific location.

        This method will copy the xclbin file into the destination directory to
        make sure DNNDK libraries can work without problems.

        The xclbin file, if not set explicitly, is required to be located
        in the same folder as the bitstream and hwh files.

        The destination folder by default is `/usr/lib`.

        """
        abs_xclbin = self.overlay_dirname + "/" + \
            self.overlay_basename.rstrip(".bit") + ".xclbin"
        if not os.path.isfile(abs_xclbin):
            raise ValueError(
                "File {} does not exist.".format(abs_xclbin))

        if not os.path.isdir(XCL_DST_PATH):
            raise ValueError(
                "Folder {} does not exist.".format(XCL_DST_PATH))
        _ = subprocess.check_output(["cp", "-f",
                                     abs_xclbin, XCL_DST_PATH])

    def load_model(self, model):
        """Load DPU models under a specific location.

        This method will compile the ML model `*.elf` binary file,
        compile it into `*.so` file located in the destination directory
        on the target. This will make sure DNNDK libraries can work
        without problems.

        The ML model file, if not set explicitly, is required to be located
        in the same folder as the bitstream and hwh files.

        The destination folder by default is `/usr/lib`.

        Currently only `*.elf` files are supported as models. The reason is
        that `*.so` usually have to be recompiled targeting a specific
        rootfs.

        Parameters
        ----------
        model : str
            The name of the ML model binary. Can be absolute or relative path.

        """
        if os.path.isfile(model):
            abs_model = model
        elif os.path.isfile(self.overlay_dirname + "/" + model):
            abs_model = self.overlay_dirname + "/" + model
        else:
            raise ValueError(
                "File {} does not exist.".format(model))
        if not os.path.isdir(XCL_DST_PATH):
            raise ValueError(
                "Folder {} does not exist.".format(XCL_DST_PATH))

        if not model.endswith(".elf"):
            raise RuntimeError("Currently only elf files can be loaded.")
        else:
            kernel_name = get_kernel_name_from_elf(abs_model)
            model_so = "libdpumodel{}.so".format(kernel_name)
            _ = subprocess.check_output(
                ["gcc", "-fPIC", "-shared", abs_model, "-o",
                 os.path.join(XCL_DST_PATH, model_so)])
