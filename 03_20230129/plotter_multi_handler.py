import os
import plotter_multi
import pandas as pd


dirname = os.path.dirname(os.path.abspath(__file__))
dir_src = os.path.join(dirname, "src/multi_file")
obj_dir = os.path.join(dirname, "obj")
dict_ = {
    "$n=2$": "d2",
    "$n=3$": "d3",
    "$n=4$": "d4",
    "$n=5$": "d5",
    "$n=6$": "d6"
}

obj_filename = "multi_file.png"

mp = plotter_multi.MyPlotter(
    obj_dir=obj_dir,
    obj_filename=obj_filename,
    step_xticks=10, step_yticks=0.5,
    FIG_SIZE=(10, 5),
    legend=True,
    x_min=0, x_max=80
)
mp.prepare_fig_ax()
for key, val in dict_.items():
    print("#", key, val)
    array = pd.read_csv(
        os.path.join(dir_src, val + ".csv"),
        header=0, index_col=0
    ).to_numpy().T[0]
    mp.plot_y(array, label=key)
mp.set_everything()
mp.save_fig()
