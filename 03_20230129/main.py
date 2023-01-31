import plotter_2
import os


plot_setting_list = []

# パス関連
dirname = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(dirname, "")
obj_dir = os.path.join(dirname, "")
tmp = "test"
src_filename = tmp + ".csv"
obj_filename = tmp + ".png"
src_path = os.path.join(src_dir, src_filename)
obj_path = os.path.join(obj_dir, obj_filename)

# ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
# header = None
# index_col = None
header = 0
index_col = 0

# step_*ticks
step_xticks = 10
step_yticks = 0.5

plot_setting_list.append(
    [
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks
    ]
)

for plot_setting in plot_setting_list:
    src_dir, src_filename, obj_dir, obj_filename, header, index_col, step_xticks, step_yticks = plot_setting
    mp = plotter_2.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks
    )
