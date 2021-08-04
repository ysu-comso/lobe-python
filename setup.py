from setuptools import setup, find_packages
import sys
import pathlib
import platform

parent = pathlib.Path(__file__).parent
# get the readme for use in our long description
readme = (parent / "README.md").read_text()

python_version = platform.python_version().rsplit('.', maxsplit=1)[0]

mac_v, _, _ = platform.mac_ver()
if mac_v != '':
    mac_version = '.'.join(mac_v.split('.')[:2])
else:
    mac_version = None

requirements = [
    "pillow>=8.1.1",
    "requests",
    "numpy~=1.19.3",
]
tf_req = "tensorflow~=2.4;platform_machine!='armv7l'"
onnx_req = "onnxruntime~=1.7.0;platform_machine!='armv7l'"
tflite_req = None

# get the right TF Lite runtime packages based on OS and python version: https://www.tensorflow.org/lite/guide/python#install_just_the_tensorflow_lite_interpreter
tflite_python = None
tflite_machine = None

# get the right python string for the version
if python_version == '3.5':
    tflite_python = 'cp35-cp35m'
elif python_version == '3.6':
    tflite_python = 'cp36-cp36m'
elif python_version == '3.7':
    tflite_python = 'cp37-cp37m'
elif python_version == '3.8':
    tflite_python = 'cp38-cp38'

# get the right machine string
if sys.platform == 'linux' and platform.machine() == 'armv7l':
    tflite_machine = 'linux_armv7l'

# add it to the requirements, or print the location to find the version to install
if tflite_python and tflite_machine:
    tflite_req = f"tflite_runtime @ https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-{tflite_python}-{tflite_machine}.whl"
else:
    tflite_req = "tflite_runtime"

setup(
    name="lobe",
    version="0.4.1",
    description="Lobe Python SDK",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/lobe/lobe-python",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={
        'full': [tf_req, onnx_req, tflite_req],
        'tf': [tf_req],
        'onnx': [onnx_req],
        'tflite': [tflite_req],
    },
    dependency_links=[
        'https://google-coral.github.io/py-repo/'
    ]
)
