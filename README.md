# Termpaper Code

https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

## Setup environment
System packages
```bash
sudo apt install -y cmake
```
Python venv
```bash
virtualenv venv -p python3
source venv/bin/activate
```
Dlib without GPU support (optional)
```bash
pip install dlib
```
Dlib with GPU support (optional)
```bash
git clone https://github.com/davisking/dlib.git
cd dlib
git checkout 237746fc1350c9091c4fb453ac62b3d2d505c8e4
mkdir build
cd build
cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
cmake --build .
cd ..
python setup.py install
```
Python packages
```bash
pip install -r requirements.txt
```


