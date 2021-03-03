#  Copyright (C) 2021 Xilinx, Inc
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


import sys
if '/usr/lib/python3.6/site-packages' not in sys.path:
    sys.path.append('/usr/lib/python3.6/site-packages')


import os
import subprocess
from ctypes import *
from typing import List
import pynq
import vart
import xir


__author__ = "Yun Rock Qu, Jingwei Zhang"
__copyright__ = "Copyright 2021, Xilinx"
__email__ = "pynq_support@xilinx.com"


MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
OVERLAY_PATH = os.path.join(MODULE_PATH, 'overlays')
XCL_DST_PATH = "/usr/lib"


def get_child_subgraph_dpu(graph: "Graph"):
    assert graph is not None, \
        "Input Graph object should not be None."
    root_subgraph = graph.get_root_subgraph()
    assert root_subgraph is not None, \
        "Failed to get root subgraph of input Graph object."
    if root_subgraph.is_leaf:
        return []
    child_subgraphs = root_subgraph.toposort_child_subgraph()
    assert child_subgraphs is not None and len(child_subgraphs) > 0
    return [cs
            for cs in child_subgraphs
            if cs.has_attr("device") and cs.get_attr("device").upper() == "DPU"]


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

        if not model.endswith(".xmodel"):
            raise RuntimeError("Currently only xmodel files can be loaded.")
        else:
            self.graph = xir.Graph.deserialize(abs_model)
            subgraphs = get_child_subgraph_dpu(self.graph)
            assert len(subgraphs) == 1
            self.runner = vart.Runner.create_runner(subgraphs[0], "run")
