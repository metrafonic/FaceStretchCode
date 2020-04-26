#!/usr/bin/env bash
rm -rf $3
for d in $1* ; do
    setting="$(basename $d)"
    mkdir -p $3/$setting
    echo "Working on folder with $setting% stretch"
    echo "Running CNN $setting"
    python dlib_code.py --detection-method cnn --image $2/ --dataset $1/$setting/ --encodings $3/$setting/dlib-cnn.joblib -o $3/$setting/dlib-cnn.csv
    python dlib_code.py --detection-method hog --image $2/ --dataset $1/$setting/ --encodings $3/$setting/dlib-hog.joblib -o $3/$setting/dlib-hog.csv
    echo "Running eigenfaces $setting"
    python cv2_eigen.py $1/$setting/ $2/ $3/$setting/opencv-eigenfaces.joblib $3/$setting/opencv-eigenfaces.csv
    #echo "Running fisherfaces $setting"
    #python cv2_fisher.py $1/$setting/ $2/ $3/$setting/opencv-fisherfaces.joblib $3/$setting/opencv-fisherfaces.csv
    echo "Running lbph $setting"
    python cv2_lbph.py $1/$setting/ $2/ $3/$setting/opencv-lbph.joblib $3/$setting/opencv-lbph.csv
done
python aggregate_results.py $3
