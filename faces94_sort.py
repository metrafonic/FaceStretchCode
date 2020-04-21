import os
import sys
import glob
import shutil

infolder = sys.argv[1]
outfolder = sys.argv[2]

image_paths = glob.glob(f"{infolder}/male/*/*.jpg")
for image in image_paths:
    print(image)
    try:
        filename = os.path.basename(image)
        subject = filename.split(".")[0]
        phototype = filename.split(".")[1]
    except:
        continue
    if phototype == "1":
        dst_file = os.path.join(outfolder, "train", subject, "id.jpg")
        if not os.path.exists(os.path.dirname(dst_file)):
            os.makedirs(os.path.dirname(dst_file))
        shutil.copyfile(image, dst_file)
    else:
        dst_file = os.path.join(outfolder, "test", subject, filename)
        if not os.path.exists(os.path.dirname(dst_file)):
            os.makedirs(os.path.dirname(dst_file))
        shutil.copyfile(image, dst_file)