import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

# 設定ファイル
import plot_setting as ps


# 各種関数
def my_round(a, unit, floor=False):
    """unitで指定した単位で数字を丸める．プロットの際のlimを設定するために使える．

    Args:
        a (float): 対象
        unit (float): ユニット
        floor (bool): Trueの場合，下側に切り捨て（正でも負でも）

    Returns:
        _type_: 丸められた数値
    """
    tmp = a/unit
    if a >= 0:  # 正
        if floor:
            tmp = math.floor(tmp)
        else:
            tmp = math.ceil(tmp)
    else:  # 負
        if floor:
            tmp = math.floor(tmp)
        else:
            tmp = math.ceil(tmp)
    return tmp * unit


def return_step(y):
    x = np.arange(1, len(y.T) + 1, 1)
    return x


# ファイル，フォルダチェック
if not os.path.exists(ps.src_path):
    raise FileNotFoundError(
        f"ファイル：{ps.src_path}がないので終了します．"
    )

if not os.path.exists(ps.obj_dir):
    print(f"ディレクトリ：{ps.obj_dir}がないので作成します．")
    os.makedirs(ps.obj_dir)


# csvファイルの読み込み
df = pd.read_csv(
    ps.src_path, header=ps.header,
    index_col=ps.index_col
)
print(df.head())

# ndarrayへの変換
y = df.to_numpy()[:205].T
print(f"ndarray: {y.shape = }, {len(y) = }")

# yに対応するndarrayの生成
if not len(y) == 1:
    print(f"# {ps.column_plotted + 1}列目についてプロット")
    y = y[ps.column_plotted]
    print(f"ndarray: {y.shape = }, {len(y) = }")

# xに対応するndarrayの生成
x = return_step(y)

# x, yの最大値と最小値を確認
y_max = np.amax(y)
y_min = np.amin(y)
x_max = np.amax(x)
x_min = np.amin(x)
print(f"{y_max = }, {y_min = }")
print(f"{x_max = }, {x_min = }")

# fig, axインスタンス
fig, ax = plt.subplots(figsize=ps.FIG_SIZE)
ax.tick_params(axis='both', labelsize=ps.FONT_TICKLABELS)
ax.set_xlabel(ps.xlabel, fontsize=ps.FONT_LABELS)
ax.set_ylabel(ps.ylabel, fontsize=ps.FONT_LABELS)

# > y axis
step_yticks = 0.5  # 最大値，最小値を元に設定
y_min_rounded = my_round(y_min, step_yticks, floor=True)
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
step_xticks = 25  # 最大値，最小値を元に設定
ndarray_for_xticks = np.arange(0, len(x)+1, step=step_xticks)[1:]
ndarray_for_xticks = np.insert(ndarray_for_xticks, 0, 1)  # 0番目に1を挿入
# ndarray_for_xticks = np.arange(1, len(x)+1, step_xticks)
x_lim = [1, len(x)]
# <

# プロット:
ax.plot(x, y.T, marker='o', markersize=3, linewidth=1)

# sets
ax.set_xlim(x_lim)
ax.set_ylim(y_lim)
ax.set_yticks(ndarray_for_yticks)
ax.set_xticks(ndarray_for_xticks)
plt.grid(True)

# Save image:
fig.savefig(
    ps.obj_path,
    bbox_inches="tight", pad_inches=0.2
)
