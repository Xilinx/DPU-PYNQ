import pynq_dpu
from pynq_dpu import DpuOverlay
import numpy as np

import os, subprocess
import pytest

TEST_DIR = os.path.dirname(__file__)

def test_vart_installed():
    try:
        import vart
    except:
        assert False
        
def test_vart_version():
    output = subprocess.run(['vart_version'], stdout=subprocess.PIPE,
                        universal_newlines=True)
    assert output.returncode == 0
    
def test_pynq_dpu_version():
    assert pynq_dpu.__version__ == '2.5.0'

def test_dpu_overlay():
    try:
        ol = DpuOverlay('dpu.bit')
    except:
        assert False, "Failed to load overlay"
        
    try:
        ol.load_model(os.path.join(TEST_DIR, "models", "dpu_resnet50.xmodel"))
    except:
        assert False, "Failed to load model"
        
    
def test_run_model():
    try:
        ol = DpuOverlay('dpu.bit')
    except:
        assert False, "Failed to load overlay"
    
    try:
        ol.load_model(os.path.join(TEST_DIR, "models", "dpu_resnet50.xmodel"))
    except:
        assert False, "Failed to load model"
    
    try:
        dpu = ol.runner
    except:
        assert False, "Failed to reference runner instance"
    
    try:
        # Prepare input/output tensors
        inputTensors = dpu.get_input_tensors()
        outputTensors = dpu.get_output_tensors()

        shapeIn = tuple(inputTensors[0].dims)
        shapeOut = tuple(outputTensors[0].dims)
        outputSize = int(outputTensors[0].get_data_size() / shapeIn[0])
    except:
        assert False
    
    try:
        # Create dummy data to feed the model
        output_data = [np.zeros(shapeOut, dtype=np.float32, order="C")]
        input_data = [np.zeros(shapeIn, dtype=np.float32, order="C")]
        image = input_data[0]
    except:
        assert False

    try:
        # Run the model
        job_id = dpu.execute_async(input_data, output_data)
        dpu.wait(job_id)
        temp = [j.reshape(1, outputSize) for j in output_data]
        softmax = np.exp((temp[0][0]))
    except:
        raise Exception("Failed dpu execution")
