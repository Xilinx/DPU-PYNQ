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

__author__ = "Yun Rock Qu, Jingwei Zhang"
__copyright__ = "Copyright 2021, Xilinx"
__email__ = "pynq_support@xilinx.com"


from setuptools import setup, find_packages, Distribution
from setuptools.command.build_ext import build_ext
import shutil
import os
import platform
import re
import warnings


# temporary fix to ignore "Device Not Found" error
try:
    from pynq.utils import build_py
except RuntimeError:
    pass


# global variables
module_name = "pynq_dpu"
git_submodule_vai = "vitis-ai-git"
data_files = []


# parse version number
def find_version(file_path):
    with open(file_path, 'r') as fp:
        version_file = fp.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",  
                                  version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise NameError("Version string must be defined in {}.".format(file_path))


# extend package
def extend_package(path):
    if os.path.isdir(path):
        data_files.extend(
            [os.path.join("..", root, f)
             for root, _, files in os.walk(path) for f in files]
        )
    elif os.path.isfile(path):
        data_files.append(os.path.join("..", path))


# merge 2 folder recursively
def copy_tree(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for f in files:
            src_file = os.path.join(src_dir, f)
            dst_file = os.path.join(dst_dir, f)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


# Enforce platform-dependent distribution
class CustomDistribution(Distribution):
    def has_ext_modules(self):
        return True


# get current platform: edge
def get_platform():
    cpu = platform.processor()
    if cpu in ['armv7l', 'aarch64']:
        return "edge"
    elif cpu in ['x86_64']:
        raise OSError("Platform is not supported.")
    else:
        raise OSError("Platform is not supported.")


# get current board
def get_board():
    board_variable = os.getenv('BOARD')
    if board_variable not in ['Ultra96', 'ZCU104', 'ZCU111']:
        warnings.warn(UserWarning, "Board is not officially supported.")
    return board_variable.lower().replace('-', '')


# install vart package

def install_vart_pkg(pkg_path, edge):
    os.system('cd {0} && '
              'wget -O vitis-ai-runtime-1.3.0.pynq.tar.gz '
              '"https://www.xilinx.com/bin/public/openDownload?filename='
              'vitis-ai-runtime-1.3.0.pynq.tar.gz" && '
              'tar -xvf vitis-ai-runtime-1.3.0.pynq.tar.gz && '
              'cd {1} && '
              'apt-get install ./*.deb && '
              'cd ../ && '
              'rm -rf *.tar.gz aarch64 armv7l && '
              'sed -i "s/media\/sd-mmcblk0p1/usr\/lib/g" '
              '/etc/vart.conf'.format(pkg_path, edge))


# resolve overlay files by moving the cached copy
def resolve_overlay_d(path):
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
    have the correct overlay files in the `overlays` folder.

    """
    def run(self):
        pkg_path = os.path.join(module_name, get_platform())
        install_vart_pkg(pkg_path, platform.processor())
        build_ext.run(self)
        overlay_path = os.path.join(self.build_lib, module_name, 'overlays')
        resolve_overlay_d(overlay_path)


pkg_version = find_version('{}/__init__.py'.format(module_name))
with open("README.md", encoding='utf-8') as fh:
    readme_lines = fh.readlines()[2:7]
long_description = (''.join(readme_lines))


extend_package(os.path.join(module_name, 'overlays'))
for arch in ['edge']:
    extend_package(os.path.join(module_name, arch))


setup(
    name=module_name,
    version=pkg_version,
    description="PYNQ DPU Overlay using Vitis AI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Xilinx PYNQ Development Team',
    author_email="pynq_support@xilinx.com",
    url='https://github.com/Xilinx/DPU-PYNQ.git',
    license='Apache License 2.0',
    packages=find_packages(),
    package_data={
        "": data_files,
    },
    python_requires=">=3.6.0",
    install_requires=[
        "pynq>=2.6.0",
        "pybind11",
        "CppHeaderParser",
        "mnist"
    ],
    entry_points={
        "pynq.notebooks": [
            "pynq-dpu = {}.{}.notebooks".format(
                module_name, get_platform())
        ]
    },
    cmdclass={"build_py": build_py,
              "build_ext": BuildExtension},
    distclass=CustomDistribution
)
