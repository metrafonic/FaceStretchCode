# Termpaper Code

https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

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
R project
```bash
sudo apt install r-base
sudo R
> install.packages("ROCR")
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
DO NOT DO THIS!!!!
mogrify -format png datasets/ufi-cropped/*/*/*.pgm
rm datasets/ufi-cropped/*/*/*.pgm
rm datasets/ufi-cropped/*/*/*.txt
```

Align faces from test folder
```bash
python align.py -r datasets/ufi-cropped/test/ -d datasets/ufi-cropped-aligned/
```
Also removes images with errors/no face

Stretch faces using ffmpeg
```bash
python stretch.py datasets/ufi-cropped/test/ datasets/ufi-cropped-stretched/ 10 5
```

# Run all
```bash
time ./run_all.sh datasets/ufi-cropped-stretched/ datasets/ufi-cropped/train/ results/

```

# Face recognition pipelines

## Face recognition with openCV and deep learning

### Encode faces

We will use an existing training network to create 128 dimension embeddings on the images.

We will not train up our own as this is overkill. This dataset is trained on 3 million images of faces.

This system uses a simple "k-NN" model + votes. 

We can use the `hog` or `cnn` (default) method to detect faces in the images.

We then encoode the faces with dlib using `face_recognition.face_encodings`. I assume this is where the deep learning steps in.

The encodings are then saved to file using `pickle.dumps()`.

#### CNN

Timing: 40s (GTX1060 3GB) or <20min (i5-7600K CPU @ 3.80GHz)
```command
python encode_faces.py --detection-method cnn --dataset ./datasets/ufi-cropped/train --encodings encodings-cnn.joblib
```

```bash
python recognize_faces_dataset.py --detection-method cnn --encodings encodings-cnn.joblib --image datasets/ufi-cropped/test/ | grep True | wc -l
379
python recognize_faces_dataset.py --detection-method cnn --encodings encodings-cnn.joblib --image datasets/ufi-cropped/test/ | grep False | wc -l
226
```

#### HOG

```command
python encode_faces.py --detection-method hog --dataset ./datasets/ufi-cropped/train --encodings encodings-hog.joblib
```

```bash
375
python recognize_faces_dataset.py --detection-method hog --encodings encodings-hog.joblib --image datasets/ufi-cropped/test/ | grep False | wc -l
230
```

## Face recognition with SVM

```bash
python svm.py datasets/ufi-cropped/train/ datasets/ufi-cropped/test/ | grep True | wc -l
425
python svm.py datasets/ufi-cropped/train/ datasets/ufi-cropped/test/ | grep False | wc -l
180
```

## Single image training
Will take a long time (single thread training)
```bash
python single_image.py --cpus 4 datasets/ufi-cropped/train/ datasets/ufi-cropped/test/ | grep True | wc -l
595
python single_image.py --cpus 4 datasets/ufi-cropped/train/ datasets/ufi-cropped/test/ | grep False | wc -l
10
```