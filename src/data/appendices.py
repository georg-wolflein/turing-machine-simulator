'''Generate the appendices file with all the plots.
'''

import os
from glob import glob

from data import DATA_DIR, APPENDICES_FILE


machines = ["paren", "binadd", "binaryunary", "subword", "subword_fast"]

print("Generating {}...".format(APPENDICES_FILE))

with open(APPENDICES_FILE, "w") as f:
    f.write(r"\section{Appendices}" + "\n")
    for machine in machines:
        f.write(
            r"\subsection{Plots for the \code{" + machine.replace("_", "\\_") + r"} machine}" + "\n")
        f.write(r"\label{plots_" + machine + r"}" + "\n")
        for plot in glob(os.path.join(DATA_DIR, machine + "-*.pdf")):
            f.write(
                r"\begin{center}\includegraphics[width=\textwidth]{plots/" + os.path.basename(plot) + r"}\end{center}" + "\n")
