import os
from glob import glob

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

from data import DATA_DIR

rc("font", family="serif")
rc("text", usetex=True)

for csv_file in glob(os.path.join(DATA_DIR, "*.csv")):
    print("Generating plot for {}...".format(csv_file))
    df = pd.read_csv(csv_file, comment="#")
    series = df.groupby("n")["num_steps"].mean()
    series.plot()
    plt.rc('text.latex', preamble=r"\usepackage{amsmath}")
    with open(csv_file, "r") as f:
        title = f.readline()
        if title.startswith("#"):
            title = title[1:]
        title = title.strip()
    plt.title(r"\begin{center}" + title + r"\end{center}")
    plt.xlabel("$n$")
    plt.ylabel("mean number of steps")
    plt.tight_layout()
    plt.savefig(os.path.splitext(csv_file)[0] + ".pdf")
    plt.close()
