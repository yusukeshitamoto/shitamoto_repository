import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os.path import exists  # Check if a target file exist
import math


def csv(filename):
    return filename + ".csv"


def png(filename):
    return filename + ".png"


def my_round(a, unit, min_=False):
    """unitで指定した単位で数字を丸める．プロットの際のlimを設定するために使える．

    Args:
        a (float): 対象
        unit (float): ユニット

    Returns:
        _type_: 丸められた数値
    """
    tmp = a/unit
    if a < 0:
        tmp = math.floor(tmp)
    else:
        if min_:
            tmp = math.floor(tmp)
        else:
            tmp = math.ceil(tmp)
    return tmp * unit


dirname = os.path.dirname(os.path.abspath(__file__))
plotting = [0]  # or "all"
obj_path = os.path.join(dirname, "results")
src_path = os.path.join(dirname, "results")
filename = "J_log"
obj_filename = filename
inverse_jsp = True
header = None
index_col = None
xlabel = "$z=1$"
ylabel = "Objective function"


# > Check the existence of the file:
if not exists(os.path.join(src_path, csv(filename))):
    raise FileNotFoundError(
        f"ファイル：{os.path.join(src_path, csv(filename))}がないのでエラー．"
    )
# <

# > Font size:
# FONT_LABELS = 28
FONT_LABELS = 28
FONT_TICKLABELS = 20
FONT_LEGENDS = 16
# <

# > Font setting:
_font = 'Times New Roman'
plt.rcParams["font.family"] = _font   # Before fig, ax =...
print("# Font:", _font, "(Linuxでは無効になる;_;)")
# plt.rcParams["font.family"] = 'sans-serif'
# plt.rcParams["font.family"] = 'Serif'
plt.rcParams["mathtext.fontset"] = 'stix'         # Before fig, ax =　...
# <

# > Figure size settings:
# FIG_SIZE = (8, 5)
FIG_SIZE = (10, 5)
# <

# df to numpy arrays
df = pd.read_csv(
    os.path.join(src_path, csv(filename)), header=header,
    index_col=index_col
)
print(df.head())
y = df.to_numpy()
print(f"{y.shape = }, {len(y) = }")
x = np.arange(1, len(y) + 1, 1)
y = y.T
# x = y[0]
print(f"{y.shape = }, {len(y) = }")

# select which y to use:
if not (plotting == "all"):
    print(f"# # データ{plotting}についてプロット．")
    y = y[plotting]
    print(f"{y.shape = }, {len(y) = }")

# > fig, axインスタンス
fig, ax = plt.subplots(figsize=FIG_SIZE)
ax.tick_params(axis='both', labelsize=FONT_TICKLABELS)
ax.set_xlabel(xlabel, fontsize=FONT_LABELS)
ax.set_ylabel(ylabel, fontsize=FONT_LABELS)
# <

# > y axis
# min, maxチェック:
y_min = np.amin(y)
y_max = np.amax(y)
# step_yticks = 1.0
step_yticks = 0.5
y_min_rounded = my_round(y_min, step_yticks, min_=True)
y_max_rounded = my_round(y_max, step_yticks)
y_lim = [
    y_min_rounded,
    y_max_rounded
]
ndarray_for_yticks = np.arange(
    y_lim[0], y_lim[1] + step_yticks, step=step_yticks
)
# <

# > x axis
step_xticks = 0.5
# ndarray_for_xticks = np.arange(0, len(x)+1, step=step_xticks)[1:]
# ndarray_for_xticks = np.insert(ndarray_for_xticks, 0, 1)  # 0番目に1を挿入
ndarray_for_xticks = np.arange(-3, 3 + step_xticks, step_xticks)
x_lim = [-3, 3]
# <


# プロット:
for i in range(len(y)):
    ax.plot(x, y[i], marker='+', linestyle=None, markersize=5, linewidth=0)
# sets
ax.set_xlim(x_lim)
ax.set_ylim(y_lim)
ax.set_yticks(ndarray_for_yticks)
print(f"{ndarray_for_yticks = }")
ax.set_xticks(ndarray_for_xticks)
print(f"{ndarray_for_xticks = }")
plt.grid(True)
# Save image:
fig.savefig(
    os.path.join(obj_path, png(obj_filename)),
    bbox_inches="tight", pad_inches=0.2
)
