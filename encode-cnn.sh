#!/usr/bin/env bash
#python encode_faces.py --detection-method cnn --dataset ./datasets/ufi-cropped-aligned/0/test --encodings encodings/0/cnn.joblib
for d in $1* ; do
    setting="$(basename $d)"
    python encode_faces.py --detection-method cnn --dataset ./datasets/ufi-cropped-stretched/$setting --encodings encodings/$setting/cnn.joblib
done