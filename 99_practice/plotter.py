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
plotting = [2]  # or "all"
obj_path = dirname
src_path = dirname
filename = "test_change_max_iter"
obj_filename = filename
inverse_jsp = True
header = 0
index_col = 0
xlabel = "Max iteration"
ylabel = "Optimized value"


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

# df to numpy arrays
df = pd.read_csv(
    os.path.join(src_path, csv(filename)), header=header,
    index_col=index_col
)
print(df.head())
y = df.to_numpy()
print(f"{y.shape = }, {len(y) = }")
# x = np.arange(1, len(y) + 1, 1)
y = y.T
x = y[0]
print(f"{y.shape = }, {len(y) = }")

# select which y to use:
if not (plotting == "all"):
    print(f"# # データ{plotting}についてプロット．")
    y = - y[plotting]
    print(f"{y.shape = }, {len(y) = }")

# min, maxチェック:
y_min = np.amin(y)
y_max = np.amax(y)

# Settings:
# FIG_SIZE = (8, 5)
FIG_SIZE = (10, 5)
step_xticks = 10
# step_yticks = 1.0
step_yticks = 0.02
y_min_rounded = my_round(y_min, step_yticks, min_=True)
y_max_rounded = my_round(y_max, step_yticks)
if ((y_max_rounded - y_min_rounded)/step_yticks > 10):
    step_yticks = 1.0
y_lim = [
    y_min_rounded,
    y_max_rounded
]
ndarray_for_yticks = np.arange(
    y_lim[0], y_lim[1] + step_yticks, step=step_yticks
)

# > fig, axインスタンス
fig, ax = plt.subplots(figsize=FIG_SIZE)
ax.tick_params(axis='both', labelsize=FONT_TICKLABELS)
ax.set_xlabel(xlabel, fontsize=FONT_LABELS)
ax.set_ylabel(ylabel, fontsize=FONT_LABELS)
ax.set_xlim([10, 100])
ax.set_ylim(y_lim)
# <

# プロット:
for i in range(len(y)):
    ax.plot(x, y[i], marker='o', markersize=3, linewidth=1)

# # Legend
# ax.legend(
#     ['Sound Pressure'], fontsize=FONT_LEGENDS
# )

# > y_ticks
ax.set_yticks(ndarray_for_yticks)
# ax.set_yticks(np.arange(0, 3.6, step=0.1), minor=True)
# <

# > x_ticks
# ndarray_for_xticks = np.arange(0, len(x)+1, step=step_xticks)[1:]
# ndarray_for_xticks = np.insert(ndarray_for_xticks, 0, 1)  # 0番目に1を挿入
ndarray_for_xticks = np.arange(10, 101, 10)
print(f"{ndarray_for_xticks = }")
ax.set_xticks(ndarray_for_xticks)
# <

# > gridの設定：
plt.grid(True)
# ax.grid(which="major", alpha=0.5, axis='y')
# ax.grid(which="minor", alpha=0.1, axis='y')
# ax.grid(which="major", alpha=10, axis='x')
# ax.grid(which="minor", alpha=2, axis='x')
# ax.grid(which="minor", alpha=0.2, axis='y')
# ax.grid(which="minor", alpha=0.2, axis='x')
# <

# 手動の余白調整：
# plt.subplots_adjust(left=0.10, right=0.95, bottom=0.2, top=0.95)

# Save image:
# fig.savefig(os.path.join(obj_path, png(obj_filename)))
# subplots_adjust()を使った方法から，bbox_inches, pad_inchesのコンビネーションに変更
fig.savefig(
    os.path.join(obj_path, png(obj_filename)),
    bbox_inches="tight", pad_inches=0.2
)



