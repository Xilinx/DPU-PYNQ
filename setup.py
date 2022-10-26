# Copyright (C) 2021 Xilinx, Inc
#
# SPDX-License-Identifier: Apache-2.0

from setuptools import setup, find_packages, Distribution
from setuptools.command.build_ext import build_ext
import shutil
import os
import platform
import re
import warnings

from pynqutils.setup_utils import build_py, extend_package


# global variables
module_name = "pynq_dpu"
data_files = []
        
# Enforce platform-dependent distribution
class CustomDistribution(Distribution):
    def has_ext_modules(self):
        return True

def install_vart_pkg():
   """ Install VART packages """
   os.system('mkdir vitis-ai-runtime-2.5.0 &&'
             'cd vitis-ai-runtime-2.5.0 &&'
             'wget -O vitis-ai-runtime-2.5.0.pynq.tar.gz '
             '"https://www.xilinx.com/bin/public/openDownload?filename='
             'vitis-ai-runtime-2.5.0.pynq.tar.gz" && '
             'tar -xvf vitis-ai-runtime-2.5.0.pynq.tar.gz && '
             'apt-get install -y ./*.deb && '
             'cd ../ && '
             'sed -i "s/media\/sd-mmcblk0p1/usr\/lib/g" '
             '/etc/vart.conf')

def resolve_overlay_d(path):
    """ Resolve overlay files by moving the cached copy """
    subfolders = [os.path.abspath(f.path) for f in os.scandir(path)
                  if f.is_dir() and f.path.endswith('.d')]
    for f in subfolders:
        dst_name = f.rstrip('.d')
        file_list = [os.path.join(f, x) for x in os.listdir(f)]
        if not file_list:
            raise FileNotFoundError("Folder {} is empty.".format(f))
        shutil.copy(file_list[0], dst_name)
        shutil.rmtree(f)


class BuildExtension(build_ext):
    """A custom build extension for adding user-specific options.

    This will first install VART package targeting the current board.
    Also, a couple of link files will be resolved at the end so users
    have the correct overlay files.

    """
    def run(self):
        install_vart_pkg()
        build_ext.run(self)
        overlay_path = os.path.join(self.build_lib, module_name)
        resolve_overlay_d(overlay_path)
        test_model_path = os.path.join(self.build_lib, module_name, 'tests', 'models')
        resolve_overlay_d(test_model_path)

with open("README.md", encoding='utf-8') as fh:
    readme_lines = fh.readlines()[2:7]
long_description = (''.join(readme_lines))

extend_package(os.path.join(module_name, 'notebooks'), data_files)
extend_package(os.path.join(module_name, 'tests'), data_files)
extend_package(module_name, data_files)

setup(
    name=module_name,
    version=2.5,
    description="PYNQ DPU Overlay using Vitis AI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Xilinx PYNQ Development Team',
    url='https://github.com/Xilinx/DPU-PYNQ.git',
    license='Apache License 2.0',
    packages=find_packages(),
    package_data={
        "": data_files,
    },
    python_requires=">=3.10.0",
    install_requires=[
        "pynq>=3.0.0",
        "pybind11",
        "CppHeaderParser",
        "mnist"
    ],
    entry_points={
        "pynq.notebooks": [
            "pynq-dpu = {}.notebooks".format(
                module_name)
        ]
    },
    cmdclass={"build_py": build_py,
              "build_ext": BuildExtension},
    distclass=CustomDistribution
)
