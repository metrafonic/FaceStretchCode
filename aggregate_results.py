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
            success_rate = float(len(success_list)) / (len(lines))
            method_results[method]["x"].append(int(stretch))
            method_results[method]["y"].append(success_rate)
            faces_info = f"{os.path.splitext(csvfile_path)[0]}-faces.txt"
            if os.path.exists(faces_info):
                with open(faces_info) as f:
                    method_results[method]["faces"].append(float(1) - float(f.readlines()[0])/100)

    for method in method_results.keys():
        zip_object = zip(method_results[method]["faces"], method_results[method]["y"])
        difference = []
        for list1_i, list2_i in zip_object:
            difference.append(list1_i + list2_i)
        method_results[method]["diff"] = difference

    linetypes = ['dashed', 'dotted']
    dottypes = ['o', 'x']
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('stretch intensity - %')
    ax1.set_ylabel('TPIR')
    ax1.tick_params(axis='y')
    i = 0
    for method in method_results.keys():
        results = method_results[method]
        ax1.plot(results["x"], results["y"], label = method, linestyle=linetypes[int(i%2)], linewidth = 3)
        i += 1
    ax1.set_title("true-positive identification rate")
    ax1.legend()
    ax1.grid(True)
    plt.show()

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('stretch intensity - %')
    ax1.set_ylabel('FTE')
    ax1.tick_params(axis='y')
    i = 0
    for method in method_results.keys():
        results = method_results[method]
        ax1.plot(results["x"], results["faces"], label=method, linestyle=linetypes[int(i%2)], linewidth=3)
        i += 1
    ax1.set_title("failure-to-entrol rate")
    ax1.legend()
    ax1.grid(True)
    plt.show()

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('stretch intensity - %')
    ax1.set_ylabel('TPIR')
    ax1.tick_params(axis='y')
    i = 0
    for method in method_results.keys():
        results = method_results[method]
        ax1.plot(results["x"], results["diff"], label=method, linestyle=linetypes[int(i % 2)], linewidth=3)
        i += 1
    ax1.set_title("true-positive identification rate (adjusted)")
    ax1.legend()
    ax1.grid(True)
    plt.show()


if __name__ == "__main__":
    main()