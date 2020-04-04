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
Dlib with GPU support (optional) - Needs old gcc version
```command
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 100 --slave /usr/bin/g++ g++ /usr/bin/g++-7
```
```command
git clone https://github.com/davisking/dlib.git
cd dlib
git checkout v19.17
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
rm datasets/ufi-cropped/*/*/*.txt
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

Timing: 40s (GTX1060 3GB) or <20min (i5-7600K CPU @ 3.80GHz)
```command
python encode_faces.py --dataset ./datasets/ufi-cropped/train --encodings encodings.pickle
```

### Detect faces in still images

```bash
python recognize_faces_image.py --encodings encodings.pickle --image datasets/ufi-cropped/test/s500/10.png 
```

### Run score system

```bash
python recognize_faces_dataset.py --encodings encodings.pickle --image datasets/ufi-cropped/test/ | grep True | wc -l

379
```

## Face recognition with SVM

```bash
docker run -it -v $PWD/project:/project registry.hedberg.io/mathias/face_recognition:latest /bin/bash
cd /root/face_recognition
export dataset=/project/dataset/
```

```bash
python svm.py datasets/ufi-cropped/train/ datasets/ufi-cropped/test/ | grep True | wc -l
425
```