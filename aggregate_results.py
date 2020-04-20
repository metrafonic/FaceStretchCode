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
        for csvfile in next(os.walk(stretchdir))[2]:
            method = os.path.splitext(csvfile)[0]
            csvfile_path = os.path.join(stretchdir, csvfile)
            if not method in method_results:
                method_results[method] = {"x": [], "y": []}
            with open(csvfile_path) as f:
                lines = [line.rstrip() for line in f]
            success_r = re.compile("^1,")
            success_list = list(filter(success_r.match, lines))
            fail_r = re.compile("^0,")
            fail_list = list(filter(fail_r.match, lines))
            success_rate = float(len(success_list)*100) / (len(lines))
            method_results[method]["x"].append(int(stretch))
            method_results[method]["y"].append(success_rate)
    for method in method_results.keys():
        results = method_results[method]
        plt.plot(results["x"], results["y"], label = method, linestyle='dashed', linewidth = 2,
         marker='o', markersize=6)
    plt.legend()
    plt.xlabel('stretch intensity - %')
    plt.ylabel('successful matches - %')
    plt.show()
    print(method_results)

if __name__ == "__main__":
    main()