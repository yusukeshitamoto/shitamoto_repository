import pandas as pd
import os
import matplotlib.pyplot as plt


dirname = os.path.dirname(os.path.abspath(__file__))
dir_top = os.path.join(dirname, "20230125")
dir_obj = os.path.join(dirname, "z_viewer")
os.makedirs(dir_obj, exist_ok=True)

b = "bayes_d"
c = "cobyla_d"
name_list = [
    c + str(2),
    c + str(4),
    c + str(6),
    c + str(8),
    b + str(2),
    b + str(4),
    b + str(6),
    b + str(8)
]

for name in name_list:
    dir_main = os.path.join(dir_top, name)
    df = pd.read_csv(
        os.path.join(dir_main, "z_log.csv"),
        index_col=None, header=None
    )
    y = df.to_numpy().T
    fig, ax = plt.subplots()
    for i in range(len(y)):
        ax.plot(y[i], marker='o')
    list_for_legend = []
    for i in range(len(y)):
        list_for_legend.append("z_" + str(i))
    ax.legend(list_for_legend)
    fig.savefig(os.path.join(dir_obj, name + ".png"))
