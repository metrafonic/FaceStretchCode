# Termpaper Code

https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

## Setup environment

System packages
```command
sudo apt install -y cmake imagemagick-6.q16
```
Python venv
```command
virtualenv venv -p python3
source venv/bin/activate
```
Dlib without GPU support (optional)
```command
pip install dlib
```
Dlib with GPU support (optional)
```command
git clone https://github.com/davisking/dlib.git
cd dlib
git checkout 237746fc1350c9091c4fb453ac62b3d2d505c8e4
mkdir build
cd build
cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
cmake --build .
cd ..
python setup.py install
cd ..
```
Python packages
```command
pip install -r requirements.txt
```

## Prepare dataset

### UFI Cropped

From <http://ufi.kiv.zcu.cz/>
```bash
mkdir datasets
curl -Lo datasets/ufi-cropped.zip http://ufi.kiv.zcu.cz/ufi-cropped.zip
unzip -d datasets/ datasets/ufi-cropped.zip
```

Convert all images to png
```command
mogrify -format png datasets/ufi-cropped/*/*/*.pgm
rm datasets/ufi-cropped/*/*/*.pgm
```
