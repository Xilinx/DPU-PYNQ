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
import pathlib
import pynq
from pynq import Register
import runner
import xir.graph
import xir.subgraph


__author__ = "Yun Rock Qu, Jingwei Zhang"
__copyright__ = "Copyright 2020, Xilinx"
__email__ = "pynq_support@xilinx.com"


MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
OVERLAY_PATH = os.path.join(MODULE_PATH, 'overlays')
XCL_DST_PATH = "/usr/lib"


def get_kernel_name_for_dnndk(model):
    """Parse the kernel name out of the given elf file for DNNDK runtime.

    This method will take elf file as input, read its information, and
    return the model name.

    Parameters
    ----------
    model : str
        The name of the ML model binary. Can be absolute or relative path.

    """
    cmd = 'readelf {} -s --wide | grep ' \
        '"0000000000000000     0 FILE    LOCAL  DEFAULT  ABS  "'.format(model)
    line = subprocess.check_output(cmd, shell=True).decode()
    kernel_0 = line.split()[-1].lstrip("dpu_").rstrip(".s")
    return kernel_0[:-len('_0')] if kernel_0.endswith('_0') else kernel_0


def get_kernel_name_for_vart(model):
    """Parse the kernel name out of the given elf file for VART.

    This method will leverage the command `dpu_model_inspect` to
    return the model name.

    Parameters
    ----------
    model : str
        The name of the ML model binary. Can be absolute or relative path.

    Returns
    -------
    (str, str)
        Model name and kernel name of the given elf file.

    """
    cmd = "dpu_model_inspect {} | grep 'model_name'".format(model)
    line0 = subprocess.check_output(cmd, shell=True).decode()
    cmd = "dpu_model_inspect {} | grep 'kernel\\[0\\]'".format(model)
    line1 = subprocess.check_output(cmd, shell=True).decode()
    return line0.split('=')[-1].lstrip().rstrip(),\
        line1.split('=')[-1].lstrip().rstrip()

def get_subgraph(g):
    sub = []
    root = g.get_root_subgraph()
    
    sub = [s for s in root.children
            if s.metadata.get_attr_str("device") == "DPU"]
    return sub

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

        By default, this class will set the runtime to be `dnndk`.

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
        self.runtime = 'dnndk'
        self.runner = None
        self.graph = None

    def download(self):
        """Download the overlay.

        This method overwrites the existing `download()` method defined in
        the overlay class. It will download the bitstream, set AXI data width,
        copy xclbin and ML model files.

        """
        super().download()
        self.overlay_dirname = os.path.dirname(self.bitfile_name)
        self.overlay_basename = os.path.basename(self.bitfile_name)

        self.copy_xclbin()

    def set_runtime(self, runtime):
        """Set runtime for the DPU.

        Parameters
        ----------
        runtime: str
            Can be either `dnndk` or `vart`.

        """
        if runtime not in ['dnndk', 'vart']:
            raise ValueError('Runtime can only be dnndk or vart.')
        self.runtime = runtime

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
        """Load DPU models for both DNNDK runtime and VART.

        For DNNDK, this method will compile the ML model `*.elf` binary file,
        compile it into `*.so` file located in the destination directory
        on the target. This will make sure DNNDK libraries can work
        without problems.

        The ML model file, if not set explicitly, is required to be located
        in the same folder as the bitstream and hwh files.

        The destination folder by default is `/usr/lib`.

        Currently only `*.elf` files are supported as models. The reason is
        that `*.so` usually have to be recompiled targeting a specific
        rootfs.

        For VART, this method will automatically generate the `meta.json` file
        in the same folder as the model file.

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
            if self.runtime == 'dnndk':
                kernel_name = get_kernel_name_for_dnndk(abs_model)
                model_so = "libdpumodel{}.so".format(kernel_name)
                _ = subprocess.check_output(
                    ["gcc", "-fPIC", "-shared", abs_model, "-o",
                     os.path.join(XCL_DST_PATH, model_so)])
            elif self.runtime == 'vart':
                model_name, kernel_name = get_kernel_name_for_vart(abs_model)
                self.graph = xir.graph.Graph.deserialize(pathlib.Path(abs_model))   
                subgraphs = get_subgraph(self.graph)
                assert len(subgraphs) == 1
                self.runner = runner.Runner(subgraphs[0],"run")
            else:
                raise ValueError('Runtime can only be dnndk or vart.')
