import os
import sys
import glob
import subprocess
import time

def main():
    source_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    stretch_interval = int(sys.argv[3])
    stretch_count = int(sys.argv[4]) * 2 + 1

    for i in range(stretch_count):
        percentage = int((i - ((stretch_count -1)/2)) * stretch_interval)
        print(percentage)
        if percentage < 0:
            settings = f"iw/1:ih*0.{100-(-1*percentage)}"
        elif percentage == 0:
            settings = f"iw/1:ih/1"
        else:
            settings = f"iw*0.{100-percentage}:ih/1"
        size_dir = os.path.join(dst_dir, str(percentage))
        files = [f for f in glob.glob(os.path.join(source_dir, "**/*.png"), recursive=True)]
        for file in files:
            subject = os.path.basename(os.path.dirname(file))
            dst_file = os.path.join(size_dir, subject, "stretched.png")
            if not os.path.exists(os.path.dirname(dst_file)):
                os.makedirs(os.path.dirname(dst_file))
            cmd = f"ffmpeg -i {file} -vf scale='{settings}' {dst_file}"
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()


if __name__ == "__main__":
    main()