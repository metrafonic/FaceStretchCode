#!/usr/bin/env bash
#python cnn.py --detection-method cnn --dataset ./datasets/ufi-cropped-aligned/0/test --encodings encodings/0/cnn.joblib
for d in $1* ; do
    setting="$(basename $d)"
    mkdir -p $3/$setting
    echo "Working on folder with $setting% stretch"
    #echo "Running CNN"
    #python cnn.py --detection-method cnn --image $2/ --dataset $1/$setting --encodings encodings/$setting/cnn.joblib > $3/$setting/cnn.csv
    echo "Running eigenfaces"
    python cv2_eigen.py $1/$setting/ $2/ encodings/$setting/eigenfaces.joblib $3/$setting/eigenfaces.csv
done