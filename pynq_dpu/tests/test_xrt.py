import os
import subprocess

def test_xbutil():
    output = subprocess.run(['xbutil', '--version'], stdout=subprocess.PIPE,
                        universal_newlines=True)
    assert output.returncode == 0
    
def test_xclbinutil():
    output = subprocess.run(['xclbinutil', '-qv'], stdout=subprocess.PIPE, universal_newlines=True)
    assert output.returncode == 0

def test_devicetree_zocl_entree():
    assert os.path.exists('/sys/firmware/devicetree/base/axi/zyxclmm_drm')
    
def test_zocl_module():
    assert 'zocl' in subprocess.run(['lsmod'], stdout=subprocess.PIPE, universal_newlines=True).stdout
