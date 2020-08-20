# Face Stretch Pipeline

## Setup environment

System packages
```command
sudo apt install -y cmake imagemagick-6.q16 python3-dev
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
Dlib with GPU support (optional) - Needs old gcc version

```command
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build
cd build
cmake .. -DCMAKE_C_COMPILER=cuda-gcc -DCMAKE_CXX_COMPILER=cuda-g++
cmake --build .
cd ..
python setup.py install
cd ..
```

If you get gcc version errors:
```command
rm -rf build

# Fedora
dnf copr enable kwizart/cuda-gcc-10.1 -y
dnf install cuda-gcc cuda-gcc-c++ -y
export CC=/usr/bin/cuda-gcc
export CXX=/usr/bin/cuda-g++
# Ubuntu
# Try without this command first
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 100 --slave /usr/bin/g++ g++ /usr/bin/g++-7
```

Python packages
```command
pip install -r requirements.txt
```

## Running
### Only view results

```
python aggregate_results.py ./results-faces94-all
```

### Run full pipeline
```bash
curl -Lo datasets/faces94.zip https://cswww.essex.ac.uk/mv/allfaces/faces94.zip
unzip -d datasets/ datasets/faces94.zip
python faces94_sort.py datasets/faces94/ datasets/faces94-sorted/
mogrify -format pgm datasets/faces94-sorted/*/*/*.jpg
rm datasets/faces94-sorted/*/*/*.jpg
python stretch.py datasets/faces94-sorted/train/ datasets/faces94-sorted-stretched/ 10 4 180 200
time ./run_all.sh datasets/faces94-sorted-stretched/ datasets/faces94-sorted/test/ results-faces94-all/
```

