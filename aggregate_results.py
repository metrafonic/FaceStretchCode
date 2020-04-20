import sys
import os
import matplotlib.pyplot as plt
import re

def main():
    results_dir = sys.argv[1]
    method_results = {}
    stretches = [int(x) for x in next(os.walk(results_dir))[1]]
    stretches.sort()
    for stretch in stretches:
        stretchdir = os.path.join(results_dir, str(stretch))
        for csvfile in [file for file in list(next(os.walk(stretchdir))[2]) if ".csv" in file]:
            method = os.path.splitext(csvfile)[0]
            csvfile_path = os.path.join(stretchdir, csvfile)
            if not method in method_results:
                method_results[method] = {"x": [], "y": [], "faces": []}
            with open(csvfile_path) as f:
                lines = [line.rstrip() for line in f]
            success_r = re.compile("^1,")
            success_list = list(filter(success_r.match, lines))
            fail_r = re.compile("^0,")
            fail_list = list(filter(fail_r.match, lines))
            success_rate = float(len(success_list)*100) / (len(lines))
            method_results[method]["x"].append(int(stretch))
            method_results[method]["y"].append(success_rate)
            faces_info = f"{os.path.splitext(csvfile_path)[0]}-faces.txt"
            if os.path.exists(faces_info):
                with open(faces_info) as f:
                    method_results[method]["faces"].append(int(f.readlines()[0]))

    fig, ax1 = plt.subplots()
    ax1.set_ylim((0, 100))
    ax1.set_xlabel('stretch intensity - %')
    ax1.set_ylabel('successful matches - %')
    ax1.tick_params(axis='y')
    for method in method_results.keys():
        results = method_results[method]
        ax1.plot(results["x"], results["y"], label = method, linestyle='dashed', linewidth = 2,
         marker='o', markersize=6)
        for i_x, i_y in zip(results["x"], results["y"]):
            ax1.text(i_x, i_y, '  ({}%)'.format(int(i_y)))
    ax1.set_title("Performance")
    ax1.legend()
    plt.show()


if __name__ == "__main__":
    main()