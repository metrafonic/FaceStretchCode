import os
import sys
import glob
import shutil

infolder = sys.argv[1]
outfolder = sys.argv[2]

image_paths = glob.glob(f"{infolder}/*")
for image in image_paths:
    print(image)
    try:
        filename = os.path.basename(image)
        subject = filename.split(".")[0]
        phototype = filename.split(".")[1]
    except:
        continue
    if phototype == "centerlight":
        dst_file = os.path.join(outfolder, "train", subject, "id.gif")
        if not os.path.exists(os.path.dirname(dst_file)):
            os.makedirs(os.path.dirname(dst_file))
        shutil.copyfile(image, dst_file)
    else:
        if "txt" in filename:
            continue
        dst_file = os.path.join(outfolder, "test", subject, f"{filename}.gif")
        if not os.path.exists(os.path.dirname(dst_file)):
            os.makedirs(os.path.dirname(dst_file))
        shutil.copyfile(image, dst_file)