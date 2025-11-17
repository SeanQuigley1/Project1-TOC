import numpy as np
import matplotlib.pyplot as plt
import os
from src.helpers.constants import RESULTS_FOLDER, INPUT_FILE


def grapher(results_collection):
    # brute -> btack -> best
    input = os.path.basename(INPUT_FILE).split(".")[0]
    titles = ["SAT - Brute Force", "SAT - Backtrack", "SAT - Best Case"]
    fileNames = [f"plots_{input}_sat_brute_force_graph_surgical.jpg", f"plots_{input}_sat_backtrack_graph_surgical.jpg", f"plots_{input}_sat_best_case_graph_surgical.jpg"]
    for index, results in enumerate(results_collection):
        time, num_literals, satisfiable = helper(results)
        plt.figure
        plt.scatter(num_literals, time, color=satisfiable)
        plt.title(titles[index])
        plt.xlabel("Number of Literals")
        plt.ylabel("Time")
        plt.grid(True)
        file_path = os.path.join(RESULTS_FOLDER, fileNames[index])
        plt.savefig(file_path)


def helper(results):
    time = []
    num_literals = []
    satisfiable = []
    for values in results:
        time.append(float(values[5]))
        num_literals.append(int(values[1]))
        satisfiable.append('green' if values[4] == "S" else 'red')
    return time, num_literals, satisfiable