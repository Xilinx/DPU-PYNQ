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

__author__ = "Yun Rock Qu, Jingwei Zhang"
__copyright__ = "Copyright 2020, Xilinx"
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
dnndk_applications = {'resnet50': "dpu_resnet50_0.elf",
                      'inception_v1': "dpu_inceptionv1_0.elf",
                      'tf_yolov3_voc_py': "dpu_tf_yolov3_0.elf"}


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


# copy DNNDK applications
def copy_dnndk_samples(src, dst):
    """Copy DNNDK samples.

    We will only copy the samples that we are interested. More samples can be
    added to the `application` list. We also need to refrain from storing
    large ML models in source distribution; hence we need to remove all the
    models.

    We will just rely on downloading large ML models from Xilinx opendownload
    when installing the package; at that time we will download specific ones
    depending on the BOARD environment.

    """
    copy_tree(os.path.join(src, 'common'),
              os.path.join(dst, 'common'))
    os.remove(os.path.join(dst, 'common', 'dputils.py'))
    for app in dnndk_applications:
        src_app = os.path.join(src, app)
        dst_app = os.path.join(dst, app)
        copy_tree(src_app, dst_app)
        os.system("cd {} && ".format(dst_app) +
                  "rm -rf build.sh Makefile model_for_*")


# Customized patch
def patch_ignore_prints(file_path):
    """Patch Python file to ignore prints.

    Some Python files in DNNDK examples have too many distracting print outs.
    This helper function will patch the Python file so we can ignore print outs.

    """
    os.system('sed -i "s/print/#print/g" {}'.format(file_path))


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


# install dnndk package
def install_dnndk_pkg(pkg_path):
    os.system('cd {} && '
              'wget -O vitis-ai_v1.2_dnndk.pynq.tar.gz '
              '"https://www.xilinx.com/bin/public/openDownload?filename='
              'vitis-ai_v1.2_dnndk.pynq.tar.gz" && '
              'tar -xvf vitis-ai_v1.2_dnndk.pynq.tar.gz && '
              'cd vitis-ai_v1.2_dnndk && '
              'bash install.sh'.format(pkg_path))


# install vart package

def install_vart_pkg(pkg_path, edge):
    os.system('cd {0} && '
              'wget -O vitis-ai-runtime-1.2.pynq.tar.gz '
              '"https://www.xilinx.com/bin/public/openDownload?filename='
              'vitis-ai-runtime-1.2.pynq.tar.gz" && '
              'tar -xvf vitis-ai-runtime-1.2.pynq.tar.gz && '
              'cd {1} && '
              'apt-get install ./*.deb && '
              'cd ../ && '
              'rm -rf *.tar.gz aarch64 armv7l'.format(pkg_path, edge))


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

    This will first install DNNDK package targeting the current board.
    Also, a couple of link files will be resolved at the end so users
    have the correct overlay files in the `overlays` folder.

    """
    def run(self):
        pkg_path = os.path.join(module_name, get_platform())
        install_dnndk_pkg(pkg_path)
        install_vart_pkg(pkg_path, platform.processor())
        build_ext.run(self)
        overlay_path = os.path.join(self.build_lib, module_name, 'overlays')
        resolve_overlay_d(overlay_path)


pkg_version = find_version('{}/__init__.py'.format(module_name))
with open("README.md", encoding='utf-8') as fh:
    readme_lines = fh.readlines()[2:7]
long_description = (''.join(readme_lines))


if os.path.isdir(git_submodule_vai):
    src_img = os.path.join(git_submodule_vai,
                           'DPU-TRD/app/img')
    dst_img = os.path.join(module_name, 'edge/notebooks/img')
    dst_data = os.path.join(module_name, 'edge/notebooks/data')
    src_dnndk_samples = os.path.join(git_submodule_vai,
                                     'mpsoc/vitis_ai_dnndk_samples')
    dst_dnndk_samples = os.path.join(module_name,
                                     'edge/dnndk')

    copy_tree(src_img, dst_img)
    shutil.copy2(os.path.join(src_dnndk_samples,
                              'inception_v1_mt/image/words.txt'),
                 dst_img)
    shutil.copy2(os.path.join(src_dnndk_samples,
                              'tf_yolov3_voc_py/image/voc_classes.txt'),
                 dst_img)
    shutil.copy2(os.path.join(src_dnndk_samples, 'common/dputils.py'),
                 module_name)
    copy_dnndk_samples(src_dnndk_samples, dst_dnndk_samples)
    patch_ignore_prints(os.path.join(dst_dnndk_samples,
                        'tf_yolov3_voc_py/tf_yolov3_voc.py'))


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
